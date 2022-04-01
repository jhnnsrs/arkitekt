import contextvars
import threading
from typing import Any, Awaitable, Callable, Coroutine, Dict, List, Optional

from pydantic import Field
from arkitekt.actors.errors import ThreadedActorCancelled
from arkitekt.messages import Assignation, Provision
from arkitekt.api.schema import AssignationStatus
from arkitekt.actors.base import Actor
from concurrent.futures import ThreadPoolExecutor
import asyncio
from arkitekt.structures.serialization.actor import expand_inputs, shrink_outputs
from arkitekt.actors.vars import (
    current_assignation,
    current_janus_queue,
)
import logging
import janus
from koil.vars import current_cancel_event
from koil.helpers import run_spawned

logger = logging.getLogger(__name__)


class FunctionalActor(Actor):
    assign: Callable[..., Any]
    provide: Optional[Callable[[Provision], Awaitable[Any]]]
    unprovide: Optional[Callable[[], Awaitable[Any]]]


class FunctionalFuncActor(FunctionalActor):
    async def progress(self, value, percentage):
        await self._progress(value, percentage)

    async def on_assign(self, assignation: Assignation):
        try:
            args, kwargs = (
                await expand_inputs(
                    self.template.node,
                    assignation.args,
                    assignation.kwargs,
                    structure_registry=self.structure_registry,
                )
                if self.expand_inputs
                else (assignation.args, assignation.kwargs)
            )

            current_assignation.set(assignation)

            await self.transport.change_assignation(
                assignation.assignation,
                status=AssignationStatus.ASSIGNED,
            )

            returns = await self.assign(*args, **kwargs)

            current_assignation.set(None)

            returns = (
                await shrink_outputs(
                    self.template.node,
                    returns,
                    structure_registry=self.structure_registry,
                )
                if self.shrink_outputs
                else returns
            )

            await self.transport.change_assignation(
                assignation.assignation,
                status=AssignationStatus.RETURNED,
                returns=returns,
            )

        except asyncio.CancelledError as e:

            await self.transport.change_assignation(
                assignation.assignation, status=AssignationStatus.CANCELLED
            )

        except Exception as e:
            logger.exception(e)
            await self.transport.change_assignation(
                assignation.assignation,
                status=AssignationStatus.CRITICAL,
                message=repr(e),
            )


class FunctionalGenActor(FunctionalActor):
    async def progress(self, value, percentage):
        await self._progress(value, percentage)

    async def on_assign(self, message: Assignation):
        try:
            args, kwargs = (
                await expand_inputs(
                    self.template.node,
                    message.args,
                    message.kwargs,
                    structure_registry=self.structure_registry,
                )
                if self.expand_inputs
                else (message.args, message.kwargs)
            )

            current_assignation.set(message)

            await self.transport.change_assignation(
                message.assignation,
                status=AssignationStatus.ASSIGNED,
            )

            async for returns in self.assign(*args, **kwargs):

                returns = (
                    await shrink_outputs(
                        self.template.node,
                        returns,
                        structure_registry=self.structure_registry,
                    )
                    if self.shrink_outputs
                    else returns
                )

                await self.transport.change_assignation(
                    message.assignation, status=AssignationStatus.YIELD, returns=returns
                )

            current_assignation.set(None)

            await self.transport.change_assignation(
                message.assignation, status=AssignationStatus.DONE
            )

        except asyncio.CancelledError as e:

            await self.transport.change_assignation(
                message.assignation, status=AssignationStatus.CANCELLED, message=str(e)
            )

        except Exception as e:
            logger.error("Error in actor", exc_info=True)
            await self.transport.change_assignation(
                message.assignation, status=AssignationStatus.CRITICAL, message=str(e)
            )

            raise e


class FunctionalThreadedFuncActor(FunctionalActor):
    threadpool: ThreadPoolExecutor = Field(
        default_factory=lambda: ThreadPoolExecutor(4)
    )

    async def on_assign(self, message: Assignation):

        try:
            logger.info("Assigning Number two")
            args, kwargs = (
                await expand_inputs(
                    self.template.node,
                    message.args,
                    message.kwargs,
                    structure_registry=self.structure_registry,
                )
                if self.expand_inputs
                else (message.args, message.kwargs)
            )

            await self.transport.change_assignation(
                message.assignation,
                status=AssignationStatus.ASSIGNED,
            )

            returns = await run_spawned(self.assign, *args, **kwargs, pass_context=True)
            shrinked_returns = (
                await shrink_outputs(
                    self.template.node,
                    returns,
                    structure_registry=self.structure_registry,
                )
                if self.expand_inputs
                else (message.args, message.kwargs)
            )

            await self.transport.change_assignation(
                message.assignation,
                status=AssignationStatus.RETURNED,
                returns=shrinked_returns,
            )

        except asyncio.CancelledError as e:
            logger.info("Actor Cancelled")

            await self.transport.change_assignation(
                message.assignation, status=AssignationStatus.CANCELLED, message=str(e)
            )

        except Exception as e:
            logger.error("Error in actor", exc_info=True)
            await self.transport.change_assignation(
                message.assignation, status=AssignationStatus.CRITICAL, message=str(e)
            )


class FunctionalThreadedGenActor(FunctionalActor):
    threadpool: ThreadPoolExecutor = Field(
        default_factory=lambda: ThreadPoolExecutor(4)
    )

    async def iterate_queue(
        self, async_q: janus._AsyncQueueProxy, message: Assignation
    ):
        try:
            while True:
                val = await async_q.get()
                action = val[0]
                value = val[1]

                if action == "log":
                    raise NotImplementedError("Logging does not work right now")
                    async_q.task_done()
                if action == "yield":

                    returns = (
                        await shrink_outputs(
                            self.template.node,
                            value,
                            structure_registry=self.structure_registry,
                        )
                        if self.shrink_outputs
                        else value
                    )

                    await self.transport.change_assignation(
                        message.assignation,
                        status=AssignationStatus.YIELD,
                        returns=returns,
                    )
                    async_q.task_done()
                if action == "done":
                    await self.transport.change_assignation(
                        message.assignation,
                        status=AssignationStatus.DONE,
                    )
                    async_q.task_done()
                    break
                if action == "exception":
                    async_q.task_done()
                    raise value

        except asyncio.CancelledError as cancelled_error:
            while True:
                val = await async_q.get()
                action = val[0]
                value = val[1]
                if action == "exception":
                    async_q.task_done()
                    try:
                        raise value
                    except ThreadedActorCancelled:
                        raise cancelled_error

    def _assign_threaded(
        self,
        queue: janus._SyncQueueProxy,
        cancel_event_instance: threading.Event,
        message: Assignation,
        args: List[Any],
        kwargs: Dict[str, Any],
        parent_context: Optional[contextvars.Context],
    ):
        for var, value in parent_context.items():
            var.set(value)

        current_janus_queue.set(queue)
        current_assignation.set(message)
        current_cancel_event.set(cancel_event_instance)
        try:
            for result in self.assign(*args, **kwargs):
                queue.put(("yield", result))
                queue.join()

            queue.put(("done", "Happy doneness"))
            queue.join()

        except Exception as e:
            logger.exception(e)
            queue.put(("exception", e))
            queue.join()

        current_janus_queue.set(None)
        current_assignation.set(None)
        current_cancel_event.set(None)

    async def on_assign(self, message: Assignation):
        loop = asyncio.get_event_loop()
        queue = janus.Queue()
        event = threading.Event()

        try:
            logger.info("Assigning Number two")
            args, kwargs = (
                await expand_inputs(
                    self.template.node,
                    message.args,
                    message.kwargs,
                    structure_registry=self.structure_registry,
                )
                if self.expand_inputs
                else (message.args, message.kwargs)
            )

            await self.transport.change_assignation(
                message.assignation,
                status=AssignationStatus.ASSIGNED,
            )

            parent_context = contextvars.copy_context()

            threadedfut = loop.run_in_executor(
                self.threadpool,
                self._assign_threaded,
                queue.sync_q,
                event,
                message,
                args,
                kwargs,
                parent_context,
            )
            queuefut = self.iterate_queue(queue.async_q, message)

            try:
                await asyncio.gather(
                    asyncio.shield(threadedfut), asyncio.shield(queuefut)
                )
                queue.close()
                await queue.wait_closed()

            except asyncio.CancelledError as e:

                queuefut.cancel()  # We cancel the quefuture and are now only waiting for cancellation requests
                event.set()  # We are sending the request to the queue

                try:
                    await queuefut
                except asyncio.CancelledError as e:
                    raise e

        except asyncio.CancelledError as e:

            await self.transport.change_assignation(
                message.assignation, status=AssignationStatus.CANCELLED, message=str(e)
            )

        except Exception as e:
            await self.transport.change_assignation(
                message.assignation, status=AssignationStatus.CRITICAL, message=str(e)
            )
