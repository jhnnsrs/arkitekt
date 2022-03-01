from arkitekt.arkitekt import Arkitekt, get_current_arkitekt


def execute(operation, variables, arkitekt: Arkitekt = None):
    arkitekt = arkitekt or get_current_arkitekt(allow_global=False)
    return operation(**arkitekt.execute(operation.Meta.document, variables).data)


async def aexecute(operation, variables, arkitekt: Arkitekt = None):
    arkitekt = arkitekt or get_current_arkitekt(allow_global=False)
    x = await arkitekt.aexecute(operation.Meta.document, variables)
    return operation(**x.data)


def subscribe(operation, variables, arkitekt: Arkitekt = None):
    mikro = arkitekt or get_current_arkitekt(allow_global=False)

    for event in mikro.subscribe(operation.Meta.document, variables):
        yield operation(**event.data)


async def asubscribe(operation, variables, arkitekt: Arkitekt = None):
    mikro = arkitekt or get_current_arkitekt(allow_global=False)
    async for event in mikro.asubscribe(operation.Meta.document, variables):
        yield operation(**event.data)
