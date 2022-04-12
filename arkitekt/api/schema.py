from pydantic import BaseModel, Field
from arkitekt.funcs import aexecute, asubscribe, subscribe, execute
from enum import Enum
from typing_extensions import Literal
from typing import Any, List, Union, AsyncIterator, Optional, Iterator, Dict
from arkitekt.scalars import QString
from arkitekt.rath import ArkitektRath
from arkitekt.traits.ports import (
    StringExpander,
    IntExpander,
    ListExpander,
    StructureExpander,
    BoolExpander,
    DictExpander,
)
from rath.scalars import ID
from arkitekt.traits.node import Reserve


class AgentStatus(str, Enum):
    """An enumeration."""

    ACTIVE = "ACTIVE"
    "Active"
    DISCONNECTED = "DISCONNECTED"
    "Disconnected"
    VANILLA = "VANILLA"
    "Complete Vanilla Scenario after a forced restart of"


class LokAppGrantType(str, Enum):
    """An enumeration."""

    CLIENT_CREDENTIALS = "CLIENT_CREDENTIALS"
    "Backend (Client Credentials)"
    IMPLICIT = "IMPLICIT"
    "Implicit Grant"
    AUTHORIZATION_CODE = "AUTHORIZATION_CODE"
    "Authorization Code"
    PASSWORD = "PASSWORD"
    "Password"
    SESSION = "SESSION"
    "Django Session"


class NodeType(str, Enum):
    """An enumeration."""

    GENERATOR = "GENERATOR"
    "Generator"
    FUNCTION = "FUNCTION"
    "Function"


class ProvisionMode(str, Enum):
    """An enumeration."""

    DEBUG = "DEBUG"
    "Debug Mode (Node might be constantly evolving)"
    PRODUCTION = "PRODUCTION"
    "Production Mode (Node might be constantly evolving)"


class ReservationStatus(str, Enum):
    """An enumeration."""

    ROUTING = "ROUTING"
    "Routing (Reservation has been requested but no Topic found yet)"
    PROVIDING = "PROVIDING"
    "Providing (Reservation required the provision of a new worker)"
    WAITING = "WAITING"
    "Waiting (We are waiting for any assignable Topic to come online)"
    REROUTING = "REROUTING"
    "Rerouting (State of provisions this reservation connects to have changed and require Retouring)"
    DISCONNECTED = "DISCONNECTED"
    "Disconnect (State of provisions this reservation connects to have changed and require Retouring)"
    DISCONNECT = "DISCONNECT"
    "Disconnect (State of provisions this reservation connects to have changed and require Retouring)"
    CANCELING = "CANCELING"
    "Cancelling (Reervation is currently being cancelled)"
    ACTIVE = "ACTIVE"
    "Active (Reservation is active and accepts assignments"
    ERROR = "ERROR"
    "Error (Reservation was not able to be performed (See StatusMessage)"
    ENDED = "ENDED"
    "Ended (Reservation was ended by the the Platform and is no longer active)"
    CANCELLED = "CANCELLED"
    "Cancelled (Reservation was cancelled by user and is no longer active)"
    CRITICAL = "CRITICAL"
    "Critical (Reservation failed with an Critical Error)"


class WaiterStatus(str, Enum):
    """An enumeration."""

    ACTIVE = "ACTIVE"
    "Active"
    DISCONNECTED = "DISCONNECTED"
    "Disconnected"
    VANILLA = "VANILLA"
    "Complete Vanilla Scenario after a forced restart of"


class AssignationStatus(str, Enum):
    """An enumeration."""

    PENDING = "PENDING"
    "Pending"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    "Acknowledged"
    RETURNED = "RETURNED"
    "Assignation Returned (Only for Functions)"
    DENIED = "DENIED"
    "Denied (Assingment was rejected)"
    ASSIGNED = "ASSIGNED"
    "Was able to assign to a pod"
    PROGRESS = "PROGRESS"
    "Progress (Assignment has current Progress)"
    RECEIVED = "RECEIVED"
    "Received (Assignment was received by an agent)"
    ERROR = "ERROR"
    "Error (Retrieable)"
    CRITICAL = "CRITICAL"
    "Critical Error (No Retries available)"
    CANCEL = "CANCEL"
    "Assinment is beeing cancelled"
    CANCELING = "CANCELING"
    "Cancelling (Assingment is currently being cancelled)"
    CANCELLED = "CANCELLED"
    "Assignment has been cancelled."
    YIELD = "YIELD"
    "Assignment yielded a value (only for Generators)"
    DONE = "DONE"
    "Assignment has finished"


class AssignationLogLevel(str, Enum):
    """An enumeration."""

    CRITICAL = "CRITICAL"
    "CRITICAL Level"
    INFO = "INFO"
    "INFO Level"
    DEBUG = "DEBUG"
    "DEBUG Level"
    ERROR = "ERROR"
    "ERROR Level"
    WARN = "WARN"
    "WARN Level"
    YIELD = "YIELD"
    "YIELD Level"
    CANCEL = "CANCEL"
    "Cancel Level"
    RETURN = "RETURN"
    "YIELD Level"
    DONE = "DONE"
    "Done Level"
    EVENT = "EVENT"
    "Event Level (only handled by plugins)"


class LogLevelInput(str, Enum):
    """An enumeration."""

    CRITICAL = "CRITICAL"
    "CRITICAL Level"
    INFO = "INFO"
    "INFO Level"
    DEBUG = "DEBUG"
    "DEBUG Level"
    ERROR = "ERROR"
    "ERROR Level"
    WARN = "WARN"
    "WARN Level"
    YIELD = "YIELD"
    "YIELD Level"
    CANCEL = "CANCEL"
    "Cancel Level"
    RETURN = "RETURN"
    "YIELD Level"
    DONE = "DONE"
    "Done Level"
    EVENT = "EVENT"
    "Event Level (only handled by plugins)"


class ReservationLogLevel(str, Enum):
    """An enumeration."""

    CRITICAL = "CRITICAL"
    "CRITICAL Level"
    INFO = "INFO"
    "INFO Level"
    DEBUG = "DEBUG"
    "DEBUG Level"
    ERROR = "ERROR"
    "ERROR Level"
    WARN = "WARN"
    "WARN Level"
    YIELD = "YIELD"
    "YIELD Level"
    CANCEL = "CANCEL"
    "Cancel Level"
    RETURN = "RETURN"
    "YIELD Level"
    DONE = "DONE"
    "Done Level"
    EVENT = "EVENT"
    "Event Level (only handled by plugins)"


class ProvisionAccess(str, Enum):
    """An enumeration."""

    EXCLUSIVE = "EXCLUSIVE"
    "This Topic is Only Accessible linkable for its creating User"
    EVERYONE = "EVERYONE"
    "Everyone can link to this Topic"


class ProvisionStatus(str, Enum):
    """An enumeration."""

    PENDING = "PENDING"
    "Pending (Request has been created and waits for its initial creation)"
    BOUND = "BOUND"
    "Bound (Provision was bound to an Agent)"
    PROVIDING = "PROVIDING"
    "Providing (Request has been send to its Agent and waits for Result"
    ACTIVE = "ACTIVE"
    "Active (Provision is currently active)"
    INACTIVE = "INACTIVE"
    "Inactive (Provision is currently not active)"
    CANCELING = "CANCELING"
    "Cancelling (Provisions is currently being cancelled)"
    LOST = "LOST"
    "Lost (Subscribers to this Topic have lost their connection)"
    RECONNECTING = "RECONNECTING"
    "Reconnecting (We are trying to Reconnect to this Topic)"
    DENIED = "DENIED"
    "Denied (Provision was rejected for this User)"
    ERROR = "ERROR"
    "Error (Reservation was not able to be performed (See StatusMessage)"
    CRITICAL = "CRITICAL"
    "Critical (Provision resulted in an critical system error)"
    ENDED = "ENDED"
    "Ended (Provision was cancelled by the Platform and will no longer create Topics)"
    CANCELLED = "CANCELLED"
    "Cancelled (Provision was cancelled by the User and will no longer create Topics)"


class ProvisionLogLevel(str, Enum):
    """An enumeration."""

    CRITICAL = "CRITICAL"
    "CRITICAL Level"
    INFO = "INFO"
    "INFO Level"
    DEBUG = "DEBUG"
    "DEBUG Level"
    ERROR = "ERROR"
    "ERROR Level"
    WARN = "WARN"
    "WARN Level"
    YIELD = "YIELD"
    "YIELD Level"
    CANCEL = "CANCEL"
    "Cancel Level"
    RETURN = "RETURN"
    "YIELD Level"
    DONE = "DONE"
    "Done Level"
    EVENT = "EVENT"
    "Event Level (only handled by plugins)"


class AssignationStatusInput(str, Enum):
    """An enumeration."""

    PENDING = "PENDING"
    "Pending"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    "Acknowledged"
    RETURNED = "RETURNED"
    "Assignation Returned (Only for Functions)"
    DENIED = "DENIED"
    "Denied (Assingment was rejected)"
    ASSIGNED = "ASSIGNED"
    "Was able to assign to a pod"
    PROGRESS = "PROGRESS"
    "Progress (Assignment has current Progress)"
    RECEIVED = "RECEIVED"
    "Received (Assignment was received by an agent)"
    ERROR = "ERROR"
    "Error (Retrieable)"
    CRITICAL = "CRITICAL"
    "Critical Error (No Retries available)"
    CANCEL = "CANCEL"
    "Assinment is beeing cancelled"
    CANCELING = "CANCELING"
    "Cancelling (Assingment is currently being cancelled)"
    CANCELLED = "CANCELLED"
    "Assignment has been cancelled."
    YIELD = "YIELD"
    "Assignment yielded a value (only for Generators)"
    DONE = "DONE"
    "Assignment has finished"


class ProvisionStatusInput(str, Enum):
    """An enumeration."""

    PENDING = "PENDING"
    "Pending (Request has been created and waits for its initial creation)"
    BOUND = "BOUND"
    "Bound (Provision was bound to an Agent)"
    PROVIDING = "PROVIDING"
    "Providing (Request has been send to its Agent and waits for Result"
    ACTIVE = "ACTIVE"
    "Active (Provision is currently active)"
    INACTIVE = "INACTIVE"
    "Inactive (Provision is currently not active)"
    CANCELING = "CANCELING"
    "Cancelling (Provisions is currently being cancelled)"
    DISCONNECTED = "DISCONNECTED"
    "Lost (Subscribers to this Topic have lost their connection)"
    RECONNECTING = "RECONNECTING"
    "Reconnecting (We are trying to Reconnect to this Topic)"
    DENIED = "DENIED"
    "Denied (Provision was rejected for this User)"
    ERROR = "ERROR"
    "Error (Reservation was not able to be performed (See StatusMessage)"
    CRITICAL = "CRITICAL"
    "Critical (Provision resulted in an critical system error)"
    ENDED = "ENDED"
    "Ended (Provision was cancelled by the Platform and will no longer create Topics)"
    CANCELLED = "CANCELLED"
    "Cancelled (Provision was cancelled by the User and will no longer create Topics)"


class RepositoryType(str, Enum):
    """An enumeration."""

    APP = "APP"
    "Repository that is hosted by an App"
    MIRROR = "MIRROR"
    "Repository mirrors online Repository"


class AgentStatusInput(str, Enum):
    """An enumeration."""

    ACTIVE = "ACTIVE"
    "Active"
    DISCONNECTED = "DISCONNECTED"
    "Disconnected"
    VANILLA = "VANILLA"
    "Complete Vanilla Scenario after a forced restart of"


class NodeTypeInput(str, Enum):
    """An enumeration."""

    GENERATOR = "GENERATOR"
    "Generator"
    FUNCTION = "FUNCTION"
    "Function"


class ReservationStatusInput(str, Enum):
    """An enumeration."""

    ROUTING = "ROUTING"
    "Routing (Reservation has been requested but no Topic found yet)"
    PROVIDING = "PROVIDING"
    "Providing (Reservation required the provision of a new worker)"
    WAITING = "WAITING"
    "Waiting (We are waiting for any assignable Topic to come online)"
    REROUTING = "REROUTING"
    "Rerouting (State of provisions this reservation connects to have changed and require Retouring)"
    DISCONNECTED = "DISCONNECTED"
    "Disconnect (State of provisions this reservation connects to have changed and require Retouring)"
    DISCONNECT = "DISCONNECT"
    "Disconnect (State of provisions this reservation connects to have changed and require Retouring)"
    CANCELING = "CANCELING"
    "Cancelling (Reervation is currently being cancelled)"
    ACTIVE = "ACTIVE"
    "Active (Reservation is active and accepts assignments"
    ERROR = "ERROR"
    "Error (Reservation was not able to be performed (See StatusMessage)"
    ENDED = "ENDED"
    "Ended (Reservation was ended by the the Platform and is no longer active)"
    CANCELLED = "CANCELLED"
    "Cancelled (Reservation was cancelled by user and is no longer active)"
    CRITICAL = "CRITICAL"
    "Critical (Reservation failed with an Critical Error)"


class ArgPortInput(BaseModel):
    key: Optional[str]
    "The Key"
    type: Optional[str]
    "the type of input"
    typename: Optional[str]
    "the type of input"
    description: Optional[str]
    "A description for this Port"
    identifier: Optional[str]
    "The corresponding Model"
    widget: Optional["WidgetInput"]
    "Which Widget to use to render Port in User Interfaces"
    label: Optional[str]
    "The corresponding label"
    child: Optional["ArgPortInput"]
    "The Child of this"
    options: Optional[Dict]
    "Options for an Enum"


class WidgetInput(BaseModel):
    typename: str
    "type"
    query: Optional[str]
    "Do we have a possible"
    dependencies: Optional[List[Optional[str]]]
    "The dependencies of this port"
    max: Optional[int]
    "Max value for int widget"
    min: Optional[int]
    "Max value for int widget"
    placeholder: Optional[str]
    "Placeholder for any widget"


class KwargPortInput(BaseModel):
    key: Optional[str]
    "The Key"
    type: Optional[str]
    "the type of input"
    typename: Optional[str]
    "the type of input"
    description: Optional[str]
    "A description for this Port"
    label: Optional[str]
    "The corresponding label"
    default_dict: Optional[Dict] = Field(alias="defaultDict")
    "Does this field have a specific value"
    default_option: Optional[Dict] = Field(alias="defaultOption")
    "Does this field have a specific value"
    default_int: Optional[int] = Field(alias="defaultInt")
    "Does this field have a specific value"
    default_bool: Optional[bool] = Field(alias="defaultBool")
    "Does this field have a specific value"
    default_float: Optional[float] = Field(alias="defaultFloat")
    "Does this field have a specific value"
    default_id: Optional[ID] = Field(alias="defaultID")
    "Does this field have a specific value"
    default_string: Optional[str] = Field(alias="defaultString")
    "Does this field have a specific value"
    default_list: Optional[List[Optional[Dict]]] = Field(alias="defaultList")
    "Does this field have a specific value"
    identifier: Optional[str]
    "The corresponding Model"
    widget: Optional["WidgetInput"]
    "Which Widget to use to render Port in User Interfaces"
    child: Optional["KwargPortInput"]
    "The Child of this"
    options: Optional[Dict]
    "Options for an Enum"


class ReturnPortInput(BaseModel):
    key: Optional[str]
    "The Key"
    type: Optional[str]
    "the type of input"
    typename: Optional[str]
    "the type of input"
    description: Optional[str]
    "A description for this Port"
    label: Optional[str]
    "The corresponding label"
    identifier: Optional[str]
    "The corresponding Model"
    child: Optional["ReturnPortInput"]
    "The Child of this"


class DefinitionInput(BaseModel):
    """A definition for a node"""

    description: Optional[str]
    "A description for the Node"
    name: str
    "The name of this template"
    args: Optional[List[Optional["ArgPortInput"]]]
    "The Args"
    kwargs: Optional[List[Optional["KwargPortInput"]]]
    "The Kwargs"
    returns: Optional[List[Optional["ReturnPortInput"]]]
    "The Returns"
    interfaces: Optional[List[Optional[str]]]
    "The Interfaces this node provides [eg. bridge, filter]"
    type: "NodeTypeInput"
    "The variety"
    interface: str
    "The Interface"
    package: Optional[str]
    "The Package"


class ReserveParamsInput(BaseModel):
    auto_provide: Optional[bool] = Field(alias="autoProvide")
    "Do you want to autoprovide"
    auto_unprovide: Optional[bool] = Field(alias="autoUnprovide")
    "Do you want to auto_unprovide"
    registries: Optional[List[Optional[ID]]]
    "Registry thar are allowed"
    agents: Optional[List[Optional[ID]]]
    "Agents that are allowed"
    templates: Optional[List[Optional[ID]]]
    "Templates that can be selected"
    desired_instances: Optional[int] = Field(alias="desiredInstances")
    "The desired amount of Instances"
    minimal_instances: Optional[int] = Field(alias="minimalInstances")
    "The minimal amount of Instances"


ReturnPortInput.update_forward_refs()
ArgPortInput.update_forward_refs()
KwargPortInput.update_forward_refs()
WidgetInput.update_forward_refs()


class AssignationFragmentParent(BaseModel):
    typename: Optional[Literal["Assignation"]] = Field(alias="__typename")
    id: ID

    class Config:
        frozen = True


class AssignationFragment(BaseModel):
    typename: Optional[Literal["Assignation"]] = Field(alias="__typename")
    args: Optional[List[Optional[Any]]]
    kwargs: Optional[Dict]
    id: ID
    parent: Optional[AssignationFragmentParent]
    "The Assignations parent"
    id: ID
    status: AssignationStatus
    "Current lifecycle of Assignation"
    statusmessage: str
    "Clear Text status of the Assignation as for now"

    class Config:
        frozen = True


class StringArgPortFragment(StringExpander, BaseModel):
    typename: Optional[Literal["StringArgPort"]] = Field(alias="__typename")
    key: Optional[str]

    class Config:
        frozen = True


class IntArgPortFragment(IntExpander, BaseModel):
    typename: Optional[Literal["IntArgPort"]] = Field(alias="__typename")
    key: Optional[str]

    class Config:
        frozen = True


class StructureArgPortFragment(StructureExpander, BaseModel):
    typename: Optional[Literal["StructureArgPort"]] = Field(alias="__typename")
    key: Optional[str]
    identifier: Optional[str]
    "The identifier of this Model"

    class Config:
        frozen = True


class ListArgPortFragmentChildBase(BaseModel):
    pass

    class Config:
        frozen = True


class ListArgPortFragmentChildStructureArgPortFragment(
    StructureExpander, ListArgPortFragmentChildBase
):
    typename: Optional[Literal["StructureArgPort"]] = Field(alias="__typename")
    identifier: Optional[str]
    "The identifier of this Model"

    class Config:
        frozen = True


class ListArgPortFragmentChildIntArgPortFragment(
    IntExpander, ListArgPortFragmentChildBase
):
    typename: Optional[Literal["IntArgPort"]] = Field(alias="__typename")

    class Config:
        frozen = True


class ListArgPortFragmentChildBoolArgPortFragment(
    BoolExpander, ListArgPortFragmentChildBase
):
    typename: Optional[Literal["BoolArgPort"]] = Field(alias="__typename")

    class Config:
        frozen = True


class ListArgPortFragmentChildStringArgPortFragment(
    StringExpander, ListArgPortFragmentChildBase
):
    typename: Optional[Literal["StringArgPort"]] = Field(alias="__typename")

    class Config:
        frozen = True


class ListArgPortFragment(ListExpander, BaseModel):
    typename: Optional[Literal["ListArgPort"]] = Field(alias="__typename")
    key: Optional[str]
    child: Optional[
        Union[
            ListArgPortFragmentChildStructureArgPortFragment,
            ListArgPortFragmentChildIntArgPortFragment,
            ListArgPortFragmentChildBoolArgPortFragment,
            ListArgPortFragmentChildStringArgPortFragment,
        ]
    ]
    "The child"

    class Config:
        frozen = True


class DictArgPortFragmentChildBase(BaseModel):
    pass

    class Config:
        frozen = True


class DictArgPortFragmentChildStructureArgPortFragment(
    StructureExpander, DictArgPortFragmentChildBase
):
    typename: Optional[Literal["StructureArgPort"]] = Field(alias="__typename")
    identifier: Optional[str]
    "The identifier of this Model"

    class Config:
        frozen = True


class DictArgPortFragmentChildIntArgPortFragment(
    IntExpander, DictArgPortFragmentChildBase
):
    typename: Optional[Literal["IntArgPort"]] = Field(alias="__typename")

    class Config:
        frozen = True


class DictArgPortFragmentChildBoolArgPortFragment(
    BoolExpander, DictArgPortFragmentChildBase
):
    typename: Optional[Literal["BoolArgPort"]] = Field(alias="__typename")

    class Config:
        frozen = True


class DictArgPortFragmentChildStringArgPortFragment(
    StringExpander, DictArgPortFragmentChildBase
):
    typename: Optional[Literal["StringArgPort"]] = Field(alias="__typename")

    class Config:
        frozen = True


class DictArgPortFragment(DictExpander, BaseModel):
    typename: Optional[Literal["DictArgPort"]] = Field(alias="__typename")
    key: Optional[str]
    child: Optional[
        Union[
            DictArgPortFragmentChildStructureArgPortFragment,
            DictArgPortFragmentChildIntArgPortFragment,
            DictArgPortFragmentChildBoolArgPortFragment,
            DictArgPortFragmentChildStringArgPortFragment,
        ]
    ]
    "The child"

    class Config:
        frozen = True


class DictKwargPortFragmentChildBase(BaseModel):
    pass

    class Config:
        frozen = True


class DictKwargPortFragmentChildStructureKwargPortFragment(
    StructureExpander, DictKwargPortFragmentChildBase
):
    typename: Optional[Literal["StructureKwargPort"]] = Field(alias="__typename")
    identifier: Optional[str]
    "The identifier of this Model"

    class Config:
        frozen = True


class DictKwargPortFragmentChildIntKwargPortFragment(
    IntExpander, DictKwargPortFragmentChildBase
):
    typename: Optional[Literal["IntKwargPort"]] = Field(alias="__typename")

    class Config:
        frozen = True


class DictKwargPortFragmentChildBoolKwargPortFragment(
    BoolExpander, DictKwargPortFragmentChildBase
):
    typename: Optional[Literal["BoolKwargPort"]] = Field(alias="__typename")

    class Config:
        frozen = True


class DictKwargPortFragmentChildStringKwargPortFragment(
    StringExpander, DictKwargPortFragmentChildBase
):
    typename: Optional[Literal["StringKwargPort"]] = Field(alias="__typename")

    class Config:
        frozen = True


class DictKwargPortFragment(DictExpander, BaseModel):
    typename: Optional[Literal["DictKwargPort"]] = Field(alias="__typename")
    key: Optional[str]
    default_dict: Optional[Dict] = Field(alias="defaultDict")
    "TheList"
    child: Optional[
        Union[
            DictKwargPortFragmentChildStructureKwargPortFragment,
            DictKwargPortFragmentChildIntKwargPortFragment,
            DictKwargPortFragmentChildBoolKwargPortFragment,
            DictKwargPortFragmentChildStringKwargPortFragment,
        ]
    ]
    "The child"

    class Config:
        frozen = True


class BoolKwargPortFragment(BoolExpander, BaseModel):
    typename: Optional[Literal["BoolKwargPort"]] = Field(alias="__typename")
    key: Optional[str]
    default_bool: Optional[bool] = Field(alias="defaultBool")
    "Default value"

    class Config:
        frozen = True


class IntKwargPortFragment(IntExpander, BaseModel):
    typename: Optional[Literal["IntKwargPort"]] = Field(alias="__typename")
    key: Optional[str]
    default_int: Optional[int] = Field(alias="defaultInt")
    "Default value"

    class Config:
        frozen = True


class StringKwargPortFragment(StringExpander, BaseModel):
    typename: Optional[Literal["StringKwargPort"]] = Field(alias="__typename")
    key: Optional[str]
    default_string: Optional[str] = Field(alias="defaultString")
    "Default value"

    class Config:
        frozen = True


class ListKwargPortFragmentChildBase(BaseModel):
    pass

    class Config:
        frozen = True


class ListKwargPortFragmentChildStructureKwargPortFragment(
    StructureExpander, ListKwargPortFragmentChildBase
):
    typename: Optional[Literal["StructureKwargPort"]] = Field(alias="__typename")
    identifier: Optional[str]
    "The identifier of this Model"

    class Config:
        frozen = True


class ListKwargPortFragmentChildIntKwargPortFragment(
    IntExpander, ListKwargPortFragmentChildBase
):
    typename: Optional[Literal["IntKwargPort"]] = Field(alias="__typename")

    class Config:
        frozen = True


class ListKwargPortFragmentChildBoolKwargPortFragment(
    BoolExpander, ListKwargPortFragmentChildBase
):
    typename: Optional[Literal["BoolKwargPort"]] = Field(alias="__typename")

    class Config:
        frozen = True


class ListKwargPortFragmentChildStringKwargPortFragment(
    StringExpander, ListKwargPortFragmentChildBase
):
    typename: Optional[Literal["StringKwargPort"]] = Field(alias="__typename")

    class Config:
        frozen = True


class ListKwargPortFragment(ListExpander, BaseModel):
    typename: Optional[Literal["ListKwargPort"]] = Field(alias="__typename")
    key: Optional[str]
    child: Optional[
        Union[
            ListKwargPortFragmentChildStructureKwargPortFragment,
            ListKwargPortFragmentChildIntKwargPortFragment,
            ListKwargPortFragmentChildBoolKwargPortFragment,
            ListKwargPortFragmentChildStringKwargPortFragment,
        ]
    ]
    "The child"
    default_list: Optional[List[Optional[Dict]]] = Field(alias="defaultList")
    "TheList"

    class Config:
        frozen = True


class ListReturnPortFragmentChildBase(BaseModel):
    pass

    class Config:
        frozen = True


class ListReturnPortFragmentChildStructureReturnPortFragment(
    StructureExpander, ListReturnPortFragmentChildBase
):
    typename: Optional[Literal["StructureReturnPort"]] = Field(alias="__typename")
    identifier: Optional[str]
    "The identifier of this Model"

    class Config:
        frozen = True


class ListReturnPortFragmentChildStringReturnPortFragment(
    StringExpander, ListReturnPortFragmentChildBase
):
    typename: Optional[Literal["StringReturnPort"]] = Field(alias="__typename")

    class Config:
        frozen = True


class ListReturnPortFragmentChildIntReturnPortFragment(
    IntExpander, ListReturnPortFragmentChildBase
):
    typename: Optional[Literal["IntReturnPort"]] = Field(alias="__typename")

    class Config:
        frozen = True


class ListReturnPortFragmentChildBoolReturnPortFragment(
    BoolExpander, ListReturnPortFragmentChildBase
):
    typename: Optional[Literal["BoolReturnPort"]] = Field(alias="__typename")

    class Config:
        frozen = True


class ListReturnPortFragment(ListExpander, BaseModel):
    typename: Optional[Literal["ListReturnPort"]] = Field(alias="__typename")
    key: Optional[str]
    child: Optional[
        Union[
            ListReturnPortFragmentChildStructureReturnPortFragment,
            ListReturnPortFragmentChildStringReturnPortFragment,
            ListReturnPortFragmentChildIntReturnPortFragment,
            ListReturnPortFragmentChildBoolReturnPortFragment,
        ]
    ]
    "The child"

    class Config:
        frozen = True


class DictReturnPortFragmentChildBase(BaseModel):
    pass

    class Config:
        frozen = True


class DictReturnPortFragmentChildStructureReturnPortFragment(
    StructureExpander, DictReturnPortFragmentChildBase
):
    typename: Optional[Literal["StructureReturnPort"]] = Field(alias="__typename")
    identifier: Optional[str]
    "The identifier of this Model"

    class Config:
        frozen = True


class DictReturnPortFragmentChildStringReturnPortFragment(
    StringExpander, DictReturnPortFragmentChildBase
):
    typename: Optional[Literal["StringReturnPort"]] = Field(alias="__typename")

    class Config:
        frozen = True


class DictReturnPortFragmentChildIntReturnPortFragment(
    IntExpander, DictReturnPortFragmentChildBase
):
    typename: Optional[Literal["IntReturnPort"]] = Field(alias="__typename")

    class Config:
        frozen = True


class DictReturnPortFragmentChildBoolReturnPortFragment(
    BoolExpander, DictReturnPortFragmentChildBase
):
    typename: Optional[Literal["BoolReturnPort"]] = Field(alias="__typename")

    class Config:
        frozen = True


class DictReturnPortFragment(DictExpander, BaseModel):
    typename: Optional[Literal["DictReturnPort"]] = Field(alias="__typename")
    key: Optional[str]
    child: Optional[
        Union[
            DictReturnPortFragmentChildStructureReturnPortFragment,
            DictReturnPortFragmentChildStringReturnPortFragment,
            DictReturnPortFragmentChildIntReturnPortFragment,
            DictReturnPortFragmentChildBoolReturnPortFragment,
        ]
    ]
    "The child"

    class Config:
        frozen = True


class StructureReturnPortFragment(StructureExpander, BaseModel):
    typename: Optional[Literal["StructureReturnPort"]] = Field(alias="__typename")
    key: Optional[str]
    identifier: Optional[str]
    "The identifier of this Model"

    class Config:
        frozen = True


class StringReturnPortFragment(StringExpander, BaseModel):
    typename: Optional[Literal["StringReturnPort"]] = Field(alias="__typename")
    key: Optional[str]

    class Config:
        frozen = True


class IntReturnPortFragment(IntExpander, BaseModel):
    typename: Optional[Literal["IntReturnPort"]] = Field(alias="__typename")
    key: Optional[str]

    class Config:
        frozen = True


class ReturnPortFragmentBase(BaseModel):
    key: Optional[str]
    description: Optional[str]


class ReturnPortFragmentBaseListReturnPort(
    ListReturnPortFragment, ReturnPortFragmentBase
):
    pass


class ReturnPortFragmentBaseStructureReturnPort(
    StructureReturnPortFragment, ReturnPortFragmentBase
):
    pass


class ReturnPortFragmentBaseStringReturnPort(
    StringReturnPortFragment, ReturnPortFragmentBase
):
    pass


class ReturnPortFragmentBaseIntReturnPort(
    IntReturnPortFragment, ReturnPortFragmentBase
):
    pass


class ReturnPortFragmentBaseDictReturnPort(
    DictReturnPortFragment, ReturnPortFragmentBase
):
    pass


ReturnPortFragment = Union[
    ReturnPortFragmentBaseListReturnPort,
    ReturnPortFragmentBaseStructureReturnPort,
    ReturnPortFragmentBaseStringReturnPort,
    ReturnPortFragmentBaseIntReturnPort,
    ReturnPortFragmentBaseDictReturnPort,
    ReturnPortFragmentBase,
]


class KwargPortFragmentBase(BaseModel):
    key: Optional[str]
    description: Optional[str]


class KwargPortFragmentBaseDictKwargPort(DictKwargPortFragment, KwargPortFragmentBase):
    pass


class KwargPortFragmentBaseBoolKwargPort(BoolKwargPortFragment, KwargPortFragmentBase):
    pass


class KwargPortFragmentBaseIntKwargPort(IntKwargPortFragment, KwargPortFragmentBase):
    pass


class KwargPortFragmentBaseListKwargPort(ListKwargPortFragment, KwargPortFragmentBase):
    pass


class KwargPortFragmentBaseStringKwargPort(
    StringKwargPortFragment, KwargPortFragmentBase
):
    pass


KwargPortFragment = Union[
    KwargPortFragmentBaseDictKwargPort,
    KwargPortFragmentBaseBoolKwargPort,
    KwargPortFragmentBaseIntKwargPort,
    KwargPortFragmentBaseListKwargPort,
    KwargPortFragmentBaseStringKwargPort,
    KwargPortFragmentBase,
]


class ArgPortFragmentBase(BaseModel):
    key: Optional[str]
    description: Optional[str]


class ArgPortFragmentBaseStringArgPort(StringArgPortFragment, ArgPortFragmentBase):
    pass


class ArgPortFragmentBaseStructureArgPort(
    StructureArgPortFragment, ArgPortFragmentBase
):
    pass


class ArgPortFragmentBaseListArgPort(ListArgPortFragment, ArgPortFragmentBase):
    pass


class ArgPortFragmentBaseIntArgPort(IntArgPortFragment, ArgPortFragmentBase):
    pass


class ArgPortFragmentBaseDictArgPort(DictArgPortFragment, ArgPortFragmentBase):
    pass


ArgPortFragment = Union[
    ArgPortFragmentBaseStringArgPort,
    ArgPortFragmentBaseStructureArgPort,
    ArgPortFragmentBaseListArgPort,
    ArgPortFragmentBaseIntArgPort,
    ArgPortFragmentBaseDictArgPort,
    ArgPortFragmentBase,
]


class ReserveParamsFragment(BaseModel):
    typename: Optional[Literal["ReserveParams"]] = Field(alias="__typename")
    registries: Optional[List[Optional[ID]]]
    "Registry thar are allowed"
    minimal_instances: Optional[int] = Field(alias="minimalInstances")
    "The minimal amount of Instances"
    desired_instances: Optional[int] = Field(alias="desiredInstances")
    "The desired amount of Instances"

    class Config:
        frozen = True


class ReservationFragmentNode(Reserve, BaseModel):
    typename: Optional[Literal["Node"]] = Field(alias="__typename")
    id: ID
    pure: bool
    "Is this function pure. e.g can we cache the result?"

    class Config:
        frozen = True


class ReservationFragment(BaseModel):
    typename: Optional[Literal["Reservation"]] = Field(alias="__typename")
    id: ID
    statusmessage: str
    "Clear Text status of the Provision as for now"
    status: ReservationStatus
    "Current lifecycle of Reservation"
    node: Optional[ReservationFragmentNode]
    "The node this reservation connects"
    params: Optional[ReserveParamsFragment]

    class Config:
        frozen = True


class NodeFragment(Reserve, BaseModel):
    typename: Optional[Literal["Node"]] = Field(alias="__typename")
    name: str
    "The cleartext name of this Node"
    interface: str
    "Interface (think Function)"
    package: str
    "Package (think Module)"
    description: str
    "A description for the Node"
    type: NodeType
    "Function, generator? Check async Programming Textbook"
    id: ID
    args: Optional[List[Optional[ArgPortFragment]]]
    kwargs: Optional[List[Optional[KwargPortFragment]]]
    returns: Optional[List[Optional[ReturnPortFragment]]]

    class Config:
        frozen = True


class TemplateFragmentRegistryApp(BaseModel):
    typename: Optional[Literal["LokApp"]] = Field(alias="__typename")
    name: str

    class Config:
        frozen = True


class TemplateFragmentRegistryUser(BaseModel):
    typename: Optional[Literal["LokUser"]] = Field(alias="__typename")
    username: str
    "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."

    class Config:
        frozen = True


class TemplateFragmentRegistry(BaseModel):
    typename: Optional[Literal["Registry"]] = Field(alias="__typename")
    name: Optional[str]
    "DEPRECATED Will be replaced in the future: : None "
    app: Optional[TemplateFragmentRegistryApp]
    "The Associated App"
    user: Optional[TemplateFragmentRegistryUser]
    "The Associated App"

    class Config:
        frozen = True


class TemplateFragment(BaseModel):
    typename: Optional[Literal["Template"]] = Field(alias="__typename")
    id: ID
    registry: TemplateFragmentRegistry
    "The associated registry for this Template"
    node: NodeFragment
    "The node this template is implementatig"
    params: Optional[Dict]

    class Config:
        frozen = True


class TodosSubscriptionTodos(BaseModel):
    typename: Optional[Literal["TodoEvent"]] = Field(alias="__typename")
    create: Optional[AssignationFragment]
    update: Optional[AssignationFragment]
    delete: Optional[ID]

    class Config:
        frozen = True


class TodosSubscription(BaseModel):
    todos: Optional[TodosSubscriptionTodos]

    class Arguments(BaseModel):
        identifier: ID

    class Meta:
        document = "fragment Assignation on Assignation {\n  args\n  kwargs\n  id\n  parent {\n    id\n  }\n  id\n  status\n  statusmessage\n}\n\nsubscription todos($identifier: ID!) {\n  todos(identifier: $identifier) {\n    create {\n      ...Assignation\n    }\n    update {\n      ...Assignation\n    }\n    delete\n  }\n}"

    class Config:
        frozen = True


class WaiterSubscriptionReservations(BaseModel):
    typename: Optional[Literal["ReservationsEvent"]] = Field(alias="__typename")
    create: Optional[ReservationFragment]
    update: Optional[ReservationFragment]
    delete: Optional[ID]

    class Config:
        frozen = True


class WaiterSubscription(BaseModel):
    reservations: Optional[WaiterSubscriptionReservations]

    class Arguments(BaseModel):
        identifier: ID

    class Meta:
        document = "fragment ReserveParams on ReserveParams {\n  registries\n  minimalInstances\n  desiredInstances\n}\n\nfragment Reservation on Reservation {\n  id\n  statusmessage\n  status\n  node {\n    id\n    pure\n  }\n  params {\n    ...ReserveParams\n  }\n}\n\nsubscription waiter($identifier: ID!) {\n  reservations(identifier: $identifier) {\n    create {\n      ...Reservation\n    }\n    update {\n      ...Reservation\n    }\n    delete\n  }\n}"

    class Config:
        frozen = True


class TodolistQuery(BaseModel):
    todolist: Optional[List[Optional[AssignationFragment]]]

    class Arguments(BaseModel):
        app_group: Optional[ID] = None

    class Meta:
        document = "fragment Assignation on Assignation {\n  args\n  kwargs\n  id\n  parent {\n    id\n  }\n  id\n  status\n  statusmessage\n}\n\nquery todolist($appGroup: ID) {\n  todolist(appGroup: $appGroup) {\n    ...Assignation\n  }\n}"

    class Config:
        frozen = True


class Get_provisionQueryProvisionTemplateNode(Reserve, BaseModel):
    typename: Optional[Literal["Node"]] = Field(alias="__typename")
    name: str
    "The cleartext name of this Node"

    class Config:
        frozen = True


class Get_provisionQueryProvisionTemplateRegistryApp(BaseModel):
    typename: Optional[Literal["LokApp"]] = Field(alias="__typename")
    name: str

    class Config:
        frozen = True


class Get_provisionQueryProvisionTemplateRegistry(BaseModel):
    typename: Optional[Literal["Registry"]] = Field(alias="__typename")
    app: Optional[Get_provisionQueryProvisionTemplateRegistryApp]
    "The Associated App"

    class Config:
        frozen = True


class Get_provisionQueryProvisionTemplate(BaseModel):
    typename: Optional[Literal["Template"]] = Field(alias="__typename")
    id: ID
    node: Get_provisionQueryProvisionTemplateNode
    "The node this template is implementatig"
    registry: Get_provisionQueryProvisionTemplateRegistry
    "The associated registry for this Template"
    extensions: Optional[List[Optional[str]]]
    "The extentions of this template"

    class Config:
        frozen = True


class Get_provisionQueryProvisionAgentRegistry(BaseModel):
    typename: Optional[Literal["Registry"]] = Field(alias="__typename")
    id: ID
    name: Optional[str]
    "DEPRECATED Will be replaced in the future: : None "

    class Config:
        frozen = True


class Get_provisionQueryProvisionAgent(BaseModel):
    typename: Optional[Literal["Agent"]] = Field(alias="__typename")
    registry: Optional[Get_provisionQueryProvisionAgentRegistry]
    "The provide might be limited to a instance like ImageJ belonging to a specific person. Is nullable for backend users"
    name: str
    "This providers Name"
    identifier: str

    class Config:
        frozen = True


class Get_provisionQueryProvisionReservationsCreator(BaseModel):
    typename: Optional[Literal["LokUser"]] = Field(alias="__typename")
    username: str
    "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."

    class Config:
        frozen = True


class Get_provisionQueryProvisionReservationsApp(BaseModel):
    typename: Optional[Literal["LokApp"]] = Field(alias="__typename")
    name: str

    class Config:
        frozen = True


class Get_provisionQueryProvisionReservations(BaseModel):
    typename: Optional[Literal["Reservation"]] = Field(alias="__typename")
    id: ID
    reference: str
    "The Unique identifier of this Assignation"
    creator: Optional[Get_provisionQueryProvisionReservationsCreator]
    "This Reservations creator"
    app: Optional[Get_provisionQueryProvisionReservationsApp]
    "This Reservations app"

    class Config:
        frozen = True


class Get_provisionQueryProvision(BaseModel):
    typename: Optional[Literal["Provision"]] = Field(alias="__typename")
    template: Optional[Get_provisionQueryProvisionTemplate]
    "The Template for this Provision"
    agent: Optional[Get_provisionQueryProvisionAgent]
    "Is this Provision bound to a certain Agent?"
    reservations: List[Get_provisionQueryProvisionReservations]
    "The Provisions this reservation connects"

    class Config:
        frozen = True


class Get_provisionQuery(BaseModel):
    provision: Optional[Get_provisionQueryProvision]

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "query get_provision($id: ID!) {\n  provision(id: $id) {\n    template {\n      id\n      node {\n        name\n      }\n      registry {\n        app {\n          name\n        }\n      }\n      extensions\n    }\n    agent {\n      registry {\n        id\n        name\n      }\n      name\n      identifier\n    }\n    reservations {\n      id\n      reference\n      creator {\n        username\n      }\n      app {\n        name\n      }\n    }\n  }\n}"

    class Config:
        frozen = True


class Get_reservationQueryReservationTemplateRegistryApp(BaseModel):
    typename: Optional[Literal["LokApp"]] = Field(alias="__typename")
    id: ID
    name: str

    class Config:
        frozen = True


class Get_reservationQueryReservationTemplateRegistryUser(BaseModel):
    typename: Optional[Literal["LokUser"]] = Field(alias="__typename")
    id: ID
    email: str

    class Config:
        frozen = True


class Get_reservationQueryReservationTemplateRegistry(BaseModel):
    typename: Optional[Literal["Registry"]] = Field(alias="__typename")
    app: Optional[Get_reservationQueryReservationTemplateRegistryApp]
    "The Associated App"
    user: Optional[Get_reservationQueryReservationTemplateRegistryUser]
    "The Associated App"

    class Config:
        frozen = True


class Get_reservationQueryReservationTemplate(BaseModel):
    typename: Optional[Literal["Template"]] = Field(alias="__typename")
    id: ID
    registry: Get_reservationQueryReservationTemplateRegistry
    "The associated registry for this Template"

    class Config:
        frozen = True


class Get_reservationQueryReservationProvisions(BaseModel):
    typename: Optional[Literal["Provision"]] = Field(alias="__typename")
    id: ID
    status: ProvisionStatus
    "Current lifecycle of Provision"

    class Config:
        frozen = True


class Get_reservationQueryReservationNode(Reserve, BaseModel):
    typename: Optional[Literal["Node"]] = Field(alias="__typename")
    id: ID
    type: NodeType
    "Function, generator? Check async Programming Textbook"
    name: str
    "The cleartext name of this Node"

    class Config:
        frozen = True


class Get_reservationQueryReservation(BaseModel):
    typename: Optional[Literal["Reservation"]] = Field(alias="__typename")
    id: ID
    template: Optional[Get_reservationQueryReservationTemplate]
    "The template this reservation connects"
    provisions: List[Get_reservationQueryReservationProvisions]
    "The Provisions this reservation connects"
    title: Optional[str]
    "A Short Hand Way to identify this reservation for you"
    status: ReservationStatus
    "Current lifecycle of Reservation"
    id: ID
    reference: str
    "The Unique identifier of this Assignation"
    node: Optional[Get_reservationQueryReservationNode]
    "The node this reservation connects"

    class Config:
        frozen = True


class Get_reservationQuery(BaseModel):
    reservation: Optional[Get_reservationQueryReservation]

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "query get_reservation($id: ID!) {\n  reservation(id: $id) {\n    id\n    template {\n      id\n      registry {\n        app {\n          id\n          name\n        }\n        user {\n          id\n          email\n        }\n      }\n    }\n    provisions {\n      id\n      status\n    }\n    title\n    status\n    id\n    reference\n    node {\n      id\n      type\n      name\n    }\n  }\n}"

    class Config:
        frozen = True


class WaitlistQuery(BaseModel):
    waitlist: Optional[List[Optional[ReservationFragment]]]

    class Arguments(BaseModel):
        app_group: Optional[ID] = None

    class Meta:
        document = "fragment ReserveParams on ReserveParams {\n  registries\n  minimalInstances\n  desiredInstances\n}\n\nfragment Reservation on Reservation {\n  id\n  statusmessage\n  status\n  node {\n    id\n    pure\n  }\n  params {\n    ...ReserveParams\n  }\n}\n\nquery waitlist($appGroup: ID) {\n  waitlist(appGroup: $appGroup) {\n    ...Reservation\n  }\n}"

    class Config:
        frozen = True


class FindQuery(BaseModel):
    node: Optional[NodeFragment]
    "Asss\n\n    Is A query for all of these specials in the world\n    "

    class Arguments(BaseModel):
        id: Optional[ID] = None
        package: Optional[str] = None
        interface: Optional[str] = None
        template: Optional[ID] = None
        q: Optional[QString] = None

    class Meta:
        document = "fragment IntReturnPort on IntReturnPort {\n  __typename\n  key\n}\n\nfragment ListReturnPort on ListReturnPort {\n  key\n  child {\n    __typename\n    ... on StructureReturnPort {\n      __typename\n      identifier\n    }\n    ... on StringReturnPort {\n      __typename\n    }\n    ... on IntReturnPort {\n      __typename\n    }\n    ... on BoolReturnPort {\n      __typename\n    }\n  }\n}\n\nfragment StructureReturnPort on StructureReturnPort {\n  __typename\n  key\n  identifier\n}\n\nfragment BoolKwargPort on BoolKwargPort {\n  key\n  defaultBool\n}\n\nfragment StringArgPort on StringArgPort {\n  key\n}\n\nfragment DictReturnPort on DictReturnPort {\n  key\n  child {\n    __typename\n    ... on StructureReturnPort {\n      __typename\n      identifier\n    }\n    ... on StringReturnPort {\n      __typename\n    }\n    ... on IntReturnPort {\n      __typename\n    }\n    ... on BoolReturnPort {\n      __typename\n    }\n  }\n}\n\nfragment DictKwargPort on DictKwargPort {\n  key\n  defaultDict\n  child {\n    __typename\n    ... on StructureKwargPort {\n      __typename\n      identifier\n    }\n    ... on IntKwargPort {\n      __typename\n    }\n    ... on BoolKwargPort {\n      __typename\n    }\n    ... on StringKwargPort {\n      __typename\n    }\n  }\n}\n\nfragment IntArgPort on IntArgPort {\n  key\n}\n\nfragment DictArgPort on DictArgPort {\n  key\n  child {\n    __typename\n    ... on StructureArgPort {\n      __typename\n      identifier\n    }\n    ... on IntArgPort {\n      __typename\n    }\n    ... on BoolArgPort {\n      __typename\n    }\n    ... on StringArgPort {\n      __typename\n    }\n  }\n}\n\nfragment StringReturnPort on StringReturnPort {\n  __typename\n  key\n}\n\nfragment StructureArgPort on StructureArgPort {\n  key\n  identifier\n}\n\nfragment IntKwargPort on IntKwargPort {\n  key\n  defaultInt\n}\n\nfragment ListArgPort on ListArgPort {\n  key\n  child {\n    __typename\n    ... on StructureArgPort {\n      __typename\n      identifier\n    }\n    ... on IntArgPort {\n      __typename\n    }\n    ... on BoolArgPort {\n      __typename\n    }\n    ... on StringArgPort {\n      __typename\n    }\n  }\n}\n\nfragment StringKwargPort on StringKwargPort {\n  key\n  defaultString\n}\n\nfragment ListKwargPort on ListKwargPort {\n  key\n  child {\n    __typename\n    ... on StructureKwargPort {\n      __typename\n      identifier\n    }\n    ... on IntKwargPort {\n      __typename\n    }\n    ... on BoolKwargPort {\n      __typename\n    }\n    ... on StringKwargPort {\n      __typename\n    }\n  }\n  defaultList\n}\n\nfragment KwargPort on KwargPort {\n  __typename\n  key\n  description\n  ...DictKwargPort\n  ...BoolKwargPort\n  ...IntKwargPort\n  ...ListKwargPort\n  ...StringKwargPort\n}\n\nfragment ReturnPort on ReturnPort {\n  __typename\n  key\n  description\n  ...ListReturnPort\n  ...StructureReturnPort\n  ...StringReturnPort\n  ...IntReturnPort\n  ...DictReturnPort\n}\n\nfragment ArgPort on ArgPort {\n  __typename\n  key\n  description\n  ...StringArgPort\n  ...StructureArgPort\n  ...ListArgPort\n  ...IntArgPort\n  ...DictArgPort\n}\n\nfragment Node on Node {\n  name\n  interface\n  package\n  description\n  type\n  id\n  args {\n    ...ArgPort\n  }\n  kwargs {\n    ...KwargPort\n  }\n  returns {\n    ...ReturnPort\n  }\n}\n\nquery find($id: ID, $package: String, $interface: String, $template: ID, $q: QString) {\n  node(\n    id: $id\n    package: $package\n    interface: $interface\n    template: $template\n    q: $q\n  ) {\n    ...Node\n  }\n}"

    class Config:
        frozen = True


class Get_templateQuery(BaseModel):
    template: Optional[TemplateFragment]

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment IntReturnPort on IntReturnPort {\n  __typename\n  key\n}\n\nfragment ListReturnPort on ListReturnPort {\n  key\n  child {\n    __typename\n    ... on StructureReturnPort {\n      __typename\n      identifier\n    }\n    ... on StringReturnPort {\n      __typename\n    }\n    ... on IntReturnPort {\n      __typename\n    }\n    ... on BoolReturnPort {\n      __typename\n    }\n  }\n}\n\nfragment StructureReturnPort on StructureReturnPort {\n  __typename\n  key\n  identifier\n}\n\nfragment BoolKwargPort on BoolKwargPort {\n  key\n  defaultBool\n}\n\nfragment StringArgPort on StringArgPort {\n  key\n}\n\nfragment DictReturnPort on DictReturnPort {\n  key\n  child {\n    __typename\n    ... on StructureReturnPort {\n      __typename\n      identifier\n    }\n    ... on StringReturnPort {\n      __typename\n    }\n    ... on IntReturnPort {\n      __typename\n    }\n    ... on BoolReturnPort {\n      __typename\n    }\n  }\n}\n\nfragment DictKwargPort on DictKwargPort {\n  key\n  defaultDict\n  child {\n    __typename\n    ... on StructureKwargPort {\n      __typename\n      identifier\n    }\n    ... on IntKwargPort {\n      __typename\n    }\n    ... on BoolKwargPort {\n      __typename\n    }\n    ... on StringKwargPort {\n      __typename\n    }\n  }\n}\n\nfragment IntArgPort on IntArgPort {\n  key\n}\n\nfragment DictArgPort on DictArgPort {\n  key\n  child {\n    __typename\n    ... on StructureArgPort {\n      __typename\n      identifier\n    }\n    ... on IntArgPort {\n      __typename\n    }\n    ... on BoolArgPort {\n      __typename\n    }\n    ... on StringArgPort {\n      __typename\n    }\n  }\n}\n\nfragment StringReturnPort on StringReturnPort {\n  __typename\n  key\n}\n\nfragment StructureArgPort on StructureArgPort {\n  key\n  identifier\n}\n\nfragment IntKwargPort on IntKwargPort {\n  key\n  defaultInt\n}\n\nfragment ListArgPort on ListArgPort {\n  key\n  child {\n    __typename\n    ... on StructureArgPort {\n      __typename\n      identifier\n    }\n    ... on IntArgPort {\n      __typename\n    }\n    ... on BoolArgPort {\n      __typename\n    }\n    ... on StringArgPort {\n      __typename\n    }\n  }\n}\n\nfragment StringKwargPort on StringKwargPort {\n  key\n  defaultString\n}\n\nfragment ListKwargPort on ListKwargPort {\n  key\n  child {\n    __typename\n    ... on StructureKwargPort {\n      __typename\n      identifier\n    }\n    ... on IntKwargPort {\n      __typename\n    }\n    ... on BoolKwargPort {\n      __typename\n    }\n    ... on StringKwargPort {\n      __typename\n    }\n  }\n  defaultList\n}\n\nfragment KwargPort on KwargPort {\n  __typename\n  key\n  description\n  ...DictKwargPort\n  ...BoolKwargPort\n  ...IntKwargPort\n  ...ListKwargPort\n  ...StringKwargPort\n}\n\nfragment ArgPort on ArgPort {\n  __typename\n  key\n  description\n  ...StringArgPort\n  ...StructureArgPort\n  ...ListArgPort\n  ...IntArgPort\n  ...DictArgPort\n}\n\nfragment ReturnPort on ReturnPort {\n  __typename\n  key\n  description\n  ...ListReturnPort\n  ...StructureReturnPort\n  ...StringReturnPort\n  ...IntReturnPort\n  ...DictReturnPort\n}\n\nfragment Node on Node {\n  name\n  interface\n  package\n  description\n  type\n  id\n  args {\n    ...ArgPort\n  }\n  kwargs {\n    ...KwargPort\n  }\n  returns {\n    ...ReturnPort\n  }\n}\n\nfragment Template on Template {\n  id\n  registry {\n    name\n    app {\n      name\n    }\n    user {\n      username\n    }\n  }\n  node {\n    ...Node\n  }\n  params\n}\n\nquery get_template($id: ID!) {\n  template(id: $id) {\n    ...Template\n  }\n}"

    class Config:
        frozen = True


class Get_agentQueryAgentRegistry(BaseModel):
    typename: Optional[Literal["Registry"]] = Field(alias="__typename")
    id: ID
    name: Optional[str]
    "DEPRECATED Will be replaced in the future: : None "

    class Config:
        frozen = True


class Get_agentQueryAgent(BaseModel):
    typename: Optional[Literal["Agent"]] = Field(alias="__typename")
    registry: Optional[Get_agentQueryAgentRegistry]
    "The provide might be limited to a instance like ImageJ belonging to a specific person. Is nullable for backend users"
    name: str
    "This providers Name"
    identifier: str

    class Config:
        frozen = True


class Get_agentQuery(BaseModel):
    agent: Optional[Get_agentQueryAgent]

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "query get_agent($id: ID!) {\n  agent(id: $id) {\n    registry {\n      id\n      name\n    }\n    name\n    identifier\n  }\n}"

    class Config:
        frozen = True


class AssignMutation(BaseModel):
    assign: Optional[AssignationFragment]

    class Arguments(BaseModel):
        reservation: ID
        args: List[Optional[Dict]]
        kwargs: Optional[Dict] = None

    class Meta:
        document = "fragment Assignation on Assignation {\n  args\n  kwargs\n  id\n  parent {\n    id\n  }\n  id\n  status\n  statusmessage\n}\n\nmutation assign($reservation: ID!, $args: [GenericScalar]!, $kwargs: GenericScalar) {\n  assign(reservation: $reservation, args: $args, kwargs: $kwargs) {\n    ...Assignation\n  }\n}"

    class Config:
        frozen = True


class UnassignMutation(BaseModel):
    unassign: Optional[AssignationFragment]

    class Arguments(BaseModel):
        assignation: ID

    class Meta:
        document = "fragment Assignation on Assignation {\n  args\n  kwargs\n  id\n  parent {\n    id\n  }\n  id\n  status\n  statusmessage\n}\n\nmutation unassign($assignation: ID!) {\n  unassign(assignation: $assignation) {\n    ...Assignation\n  }\n}"

    class Config:
        frozen = True


class ReserveMutation(BaseModel):
    reserve: Optional[ReservationFragment]

    class Arguments(BaseModel):
        node: Optional[ID] = None
        template: Optional[ID] = None
        params: Optional[ReserveParamsInput] = None
        title: Optional[str] = None
        creator: Optional[ID] = None
        app_group: Optional[ID] = None

    class Meta:
        document = "fragment ReserveParams on ReserveParams {\n  registries\n  minimalInstances\n  desiredInstances\n}\n\nfragment Reservation on Reservation {\n  id\n  statusmessage\n  status\n  node {\n    id\n    pure\n  }\n  params {\n    ...ReserveParams\n  }\n}\n\nmutation reserve($node: ID, $template: ID, $params: ReserveParamsInput, $title: String, $creator: ID, $appGroup: ID) {\n  reserve(\n    node: $node\n    template: $template\n    params: $params\n    title: $title\n    creator: $creator\n    appGroup: $appGroup\n  ) {\n    ...Reservation\n  }\n}"

    class Config:
        frozen = True


class UnreserveMutation(BaseModel):
    unreserve: Optional[ReservationFragment]

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment ReserveParams on ReserveParams {\n  registries\n  minimalInstances\n  desiredInstances\n}\n\nfragment Reservation on Reservation {\n  id\n  statusmessage\n  status\n  node {\n    id\n    pure\n  }\n  params {\n    ...ReserveParams\n  }\n}\n\nmutation unreserve($id: ID!) {\n  unreserve(id: $id) {\n    ...Reservation\n  }\n}"

    class Config:
        frozen = True


class Create_nodeMutation(BaseModel):
    create_node: Optional[NodeFragment] = Field(alias="createNode")
    "Create Node according to the specifications"

    class Arguments(BaseModel):
        name: str
        interface: str
        args: Optional[List[Optional[ArgPortInput]]] = None

    class Meta:
        document = "fragment IntReturnPort on IntReturnPort {\n  __typename\n  key\n}\n\nfragment ListReturnPort on ListReturnPort {\n  key\n  child {\n    __typename\n    ... on StructureReturnPort {\n      __typename\n      identifier\n    }\n    ... on StringReturnPort {\n      __typename\n    }\n    ... on IntReturnPort {\n      __typename\n    }\n    ... on BoolReturnPort {\n      __typename\n    }\n  }\n}\n\nfragment StructureReturnPort on StructureReturnPort {\n  __typename\n  key\n  identifier\n}\n\nfragment BoolKwargPort on BoolKwargPort {\n  key\n  defaultBool\n}\n\nfragment StringArgPort on StringArgPort {\n  key\n}\n\nfragment DictReturnPort on DictReturnPort {\n  key\n  child {\n    __typename\n    ... on StructureReturnPort {\n      __typename\n      identifier\n    }\n    ... on StringReturnPort {\n      __typename\n    }\n    ... on IntReturnPort {\n      __typename\n    }\n    ... on BoolReturnPort {\n      __typename\n    }\n  }\n}\n\nfragment DictKwargPort on DictKwargPort {\n  key\n  defaultDict\n  child {\n    __typename\n    ... on StructureKwargPort {\n      __typename\n      identifier\n    }\n    ... on IntKwargPort {\n      __typename\n    }\n    ... on BoolKwargPort {\n      __typename\n    }\n    ... on StringKwargPort {\n      __typename\n    }\n  }\n}\n\nfragment IntArgPort on IntArgPort {\n  key\n}\n\nfragment DictArgPort on DictArgPort {\n  key\n  child {\n    __typename\n    ... on StructureArgPort {\n      __typename\n      identifier\n    }\n    ... on IntArgPort {\n      __typename\n    }\n    ... on BoolArgPort {\n      __typename\n    }\n    ... on StringArgPort {\n      __typename\n    }\n  }\n}\n\nfragment StringReturnPort on StringReturnPort {\n  __typename\n  key\n}\n\nfragment StructureArgPort on StructureArgPort {\n  key\n  identifier\n}\n\nfragment IntKwargPort on IntKwargPort {\n  key\n  defaultInt\n}\n\nfragment ListArgPort on ListArgPort {\n  key\n  child {\n    __typename\n    ... on StructureArgPort {\n      __typename\n      identifier\n    }\n    ... on IntArgPort {\n      __typename\n    }\n    ... on BoolArgPort {\n      __typename\n    }\n    ... on StringArgPort {\n      __typename\n    }\n  }\n}\n\nfragment StringKwargPort on StringKwargPort {\n  key\n  defaultString\n}\n\nfragment ListKwargPort on ListKwargPort {\n  key\n  child {\n    __typename\n    ... on StructureKwargPort {\n      __typename\n      identifier\n    }\n    ... on IntKwargPort {\n      __typename\n    }\n    ... on BoolKwargPort {\n      __typename\n    }\n    ... on StringKwargPort {\n      __typename\n    }\n  }\n  defaultList\n}\n\nfragment KwargPort on KwargPort {\n  __typename\n  key\n  description\n  ...DictKwargPort\n  ...BoolKwargPort\n  ...IntKwargPort\n  ...ListKwargPort\n  ...StringKwargPort\n}\n\nfragment ReturnPort on ReturnPort {\n  __typename\n  key\n  description\n  ...ListReturnPort\n  ...StructureReturnPort\n  ...StringReturnPort\n  ...IntReturnPort\n  ...DictReturnPort\n}\n\nfragment ArgPort on ArgPort {\n  __typename\n  key\n  description\n  ...StringArgPort\n  ...StructureArgPort\n  ...ListArgPort\n  ...IntArgPort\n  ...DictArgPort\n}\n\nfragment Node on Node {\n  name\n  interface\n  package\n  description\n  type\n  id\n  args {\n    ...ArgPort\n  }\n  kwargs {\n    ...KwargPort\n  }\n  returns {\n    ...ReturnPort\n  }\n}\n\nmutation create_node($name: String!, $interface: String!, $args: [ArgPortInput]) {\n  createNode(name: $name, interface: $interface, args: $args) {\n    ...Node\n  }\n}"

    class Config:
        frozen = True


class DefineMutation(BaseModel):
    define: Optional[NodeFragment]
    "Defines a node according to is definition"

    class Arguments(BaseModel):
        definition: DefinitionInput

    class Meta:
        document = "fragment IntReturnPort on IntReturnPort {\n  __typename\n  key\n}\n\nfragment ListReturnPort on ListReturnPort {\n  key\n  child {\n    __typename\n    ... on StructureReturnPort {\n      __typename\n      identifier\n    }\n    ... on StringReturnPort {\n      __typename\n    }\n    ... on IntReturnPort {\n      __typename\n    }\n    ... on BoolReturnPort {\n      __typename\n    }\n  }\n}\n\nfragment StructureReturnPort on StructureReturnPort {\n  __typename\n  key\n  identifier\n}\n\nfragment BoolKwargPort on BoolKwargPort {\n  key\n  defaultBool\n}\n\nfragment StringArgPort on StringArgPort {\n  key\n}\n\nfragment DictReturnPort on DictReturnPort {\n  key\n  child {\n    __typename\n    ... on StructureReturnPort {\n      __typename\n      identifier\n    }\n    ... on StringReturnPort {\n      __typename\n    }\n    ... on IntReturnPort {\n      __typename\n    }\n    ... on BoolReturnPort {\n      __typename\n    }\n  }\n}\n\nfragment DictKwargPort on DictKwargPort {\n  key\n  defaultDict\n  child {\n    __typename\n    ... on StructureKwargPort {\n      __typename\n      identifier\n    }\n    ... on IntKwargPort {\n      __typename\n    }\n    ... on BoolKwargPort {\n      __typename\n    }\n    ... on StringKwargPort {\n      __typename\n    }\n  }\n}\n\nfragment IntArgPort on IntArgPort {\n  key\n}\n\nfragment DictArgPort on DictArgPort {\n  key\n  child {\n    __typename\n    ... on StructureArgPort {\n      __typename\n      identifier\n    }\n    ... on IntArgPort {\n      __typename\n    }\n    ... on BoolArgPort {\n      __typename\n    }\n    ... on StringArgPort {\n      __typename\n    }\n  }\n}\n\nfragment StringReturnPort on StringReturnPort {\n  __typename\n  key\n}\n\nfragment StructureArgPort on StructureArgPort {\n  key\n  identifier\n}\n\nfragment IntKwargPort on IntKwargPort {\n  key\n  defaultInt\n}\n\nfragment ListArgPort on ListArgPort {\n  key\n  child {\n    __typename\n    ... on StructureArgPort {\n      __typename\n      identifier\n    }\n    ... on IntArgPort {\n      __typename\n    }\n    ... on BoolArgPort {\n      __typename\n    }\n    ... on StringArgPort {\n      __typename\n    }\n  }\n}\n\nfragment StringKwargPort on StringKwargPort {\n  key\n  defaultString\n}\n\nfragment ListKwargPort on ListKwargPort {\n  key\n  child {\n    __typename\n    ... on StructureKwargPort {\n      __typename\n      identifier\n    }\n    ... on IntKwargPort {\n      __typename\n    }\n    ... on BoolKwargPort {\n      __typename\n    }\n    ... on StringKwargPort {\n      __typename\n    }\n  }\n  defaultList\n}\n\nfragment KwargPort on KwargPort {\n  __typename\n  key\n  description\n  ...DictKwargPort\n  ...BoolKwargPort\n  ...IntKwargPort\n  ...ListKwargPort\n  ...StringKwargPort\n}\n\nfragment ReturnPort on ReturnPort {\n  __typename\n  key\n  description\n  ...ListReturnPort\n  ...StructureReturnPort\n  ...StringReturnPort\n  ...IntReturnPort\n  ...DictReturnPort\n}\n\nfragment ArgPort on ArgPort {\n  __typename\n  key\n  description\n  ...StringArgPort\n  ...StructureArgPort\n  ...ListArgPort\n  ...IntArgPort\n  ...DictArgPort\n}\n\nfragment Node on Node {\n  name\n  interface\n  package\n  description\n  type\n  id\n  args {\n    ...ArgPort\n  }\n  kwargs {\n    ...KwargPort\n  }\n  returns {\n    ...ReturnPort\n  }\n}\n\nmutation define($definition: DefinitionInput!) {\n  define(definition: $definition) {\n    ...Node\n  }\n}"

    class Config:
        frozen = True


class Reset_repositoryMutationResetrepository(BaseModel):
    typename: Optional[Literal["ResetRepositoryReturn"]] = Field(alias="__typename")
    ok: Optional[bool]

    class Config:
        frozen = True


class Reset_repositoryMutation(BaseModel):
    reset_repository: Optional[Reset_repositoryMutationResetrepository] = Field(
        alias="resetRepository"
    )
    "Create Repostiory"

    class Arguments(BaseModel):
        pass

    class Meta:
        document = "mutation reset_repository {\n  resetRepository {\n    ok\n  }\n}"

    class Config:
        frozen = True


class Create_templateMutation(BaseModel):
    create_template: Optional[TemplateFragment] = Field(alias="createTemplate")

    class Arguments(BaseModel):
        node: ID
        params: Optional[Dict] = None
        extensions: Optional[List[Optional[str]]] = None
        version: Optional[str] = None

    class Meta:
        document = "fragment IntReturnPort on IntReturnPort {\n  __typename\n  key\n}\n\nfragment ListReturnPort on ListReturnPort {\n  key\n  child {\n    __typename\n    ... on StructureReturnPort {\n      __typename\n      identifier\n    }\n    ... on StringReturnPort {\n      __typename\n    }\n    ... on IntReturnPort {\n      __typename\n    }\n    ... on BoolReturnPort {\n      __typename\n    }\n  }\n}\n\nfragment StructureReturnPort on StructureReturnPort {\n  __typename\n  key\n  identifier\n}\n\nfragment BoolKwargPort on BoolKwargPort {\n  key\n  defaultBool\n}\n\nfragment StringArgPort on StringArgPort {\n  key\n}\n\nfragment DictReturnPort on DictReturnPort {\n  key\n  child {\n    __typename\n    ... on StructureReturnPort {\n      __typename\n      identifier\n    }\n    ... on StringReturnPort {\n      __typename\n    }\n    ... on IntReturnPort {\n      __typename\n    }\n    ... on BoolReturnPort {\n      __typename\n    }\n  }\n}\n\nfragment DictKwargPort on DictKwargPort {\n  key\n  defaultDict\n  child {\n    __typename\n    ... on StructureKwargPort {\n      __typename\n      identifier\n    }\n    ... on IntKwargPort {\n      __typename\n    }\n    ... on BoolKwargPort {\n      __typename\n    }\n    ... on StringKwargPort {\n      __typename\n    }\n  }\n}\n\nfragment IntArgPort on IntArgPort {\n  key\n}\n\nfragment DictArgPort on DictArgPort {\n  key\n  child {\n    __typename\n    ... on StructureArgPort {\n      __typename\n      identifier\n    }\n    ... on IntArgPort {\n      __typename\n    }\n    ... on BoolArgPort {\n      __typename\n    }\n    ... on StringArgPort {\n      __typename\n    }\n  }\n}\n\nfragment StringReturnPort on StringReturnPort {\n  __typename\n  key\n}\n\nfragment StructureArgPort on StructureArgPort {\n  key\n  identifier\n}\n\nfragment IntKwargPort on IntKwargPort {\n  key\n  defaultInt\n}\n\nfragment ListArgPort on ListArgPort {\n  key\n  child {\n    __typename\n    ... on StructureArgPort {\n      __typename\n      identifier\n    }\n    ... on IntArgPort {\n      __typename\n    }\n    ... on BoolArgPort {\n      __typename\n    }\n    ... on StringArgPort {\n      __typename\n    }\n  }\n}\n\nfragment StringKwargPort on StringKwargPort {\n  key\n  defaultString\n}\n\nfragment ListKwargPort on ListKwargPort {\n  key\n  child {\n    __typename\n    ... on StructureKwargPort {\n      __typename\n      identifier\n    }\n    ... on IntKwargPort {\n      __typename\n    }\n    ... on BoolKwargPort {\n      __typename\n    }\n    ... on StringKwargPort {\n      __typename\n    }\n  }\n  defaultList\n}\n\nfragment KwargPort on KwargPort {\n  __typename\n  key\n  description\n  ...DictKwargPort\n  ...BoolKwargPort\n  ...IntKwargPort\n  ...ListKwargPort\n  ...StringKwargPort\n}\n\nfragment ArgPort on ArgPort {\n  __typename\n  key\n  description\n  ...StringArgPort\n  ...StructureArgPort\n  ...ListArgPort\n  ...IntArgPort\n  ...DictArgPort\n}\n\nfragment ReturnPort on ReturnPort {\n  __typename\n  key\n  description\n  ...ListReturnPort\n  ...StructureReturnPort\n  ...StringReturnPort\n  ...IntReturnPort\n  ...DictReturnPort\n}\n\nfragment Node on Node {\n  name\n  interface\n  package\n  description\n  type\n  id\n  args {\n    ...ArgPort\n  }\n  kwargs {\n    ...KwargPort\n  }\n  returns {\n    ...ReturnPort\n  }\n}\n\nfragment Template on Template {\n  id\n  registry {\n    name\n    app {\n      name\n    }\n    user {\n      username\n    }\n  }\n  node {\n    ...Node\n  }\n  params\n}\n\nmutation create_template($node: ID!, $params: GenericScalar, $extensions: [String], $version: String) {\n  createTemplate(\n    node: $node\n    params: $params\n    extensions: $extensions\n    version: $version\n  ) {\n    ...Template\n  }\n}"

    class Config:
        frozen = True


class SlateMutation(BaseModel):
    slate: Optional[List[Optional[ID]]]

    class Arguments(BaseModel):
        identifier: str

    class Meta:
        document = "mutation slate($identifier: String!) {\n  slate(identifier: $identifier)\n}"

    class Config:
        frozen = True


async def atodos(
    identifier: Optional[ID], rath: ArkitektRath = None
) -> AsyncIterator[Optional[TodosSubscriptionTodos]]:
    """todos



    Arguments:
        identifier (ID): identifier
        rath (arkitekt.rath.ArkitektRath, optional): The arkitekt rath client

    Returns:
        TodosSubscription"""
    async for event in asubscribe(
        TodosSubscription, {"identifier": identifier}, rath=rath
    ):
        yield event.todos


def todos(
    identifier: Optional[ID], rath: ArkitektRath = None
) -> Iterator[Optional[TodosSubscriptionTodos]]:
    """todos



    Arguments:
        identifier (ID): identifier
        rath (arkitekt.rath.ArkitektRath, optional): The arkitekt rath client

    Returns:
        TodosSubscription"""
    for event in subscribe(TodosSubscription, {"identifier": identifier}, rath=rath):
        yield event.todos


async def awaiter(
    identifier: Optional[ID], rath: ArkitektRath = None
) -> AsyncIterator[Optional[WaiterSubscriptionReservations]]:
    """waiter



    Arguments:
        identifier (ID): identifier
        rath (arkitekt.rath.ArkitektRath, optional): The arkitekt rath client

    Returns:
        WaiterSubscription"""
    async for event in asubscribe(
        WaiterSubscription, {"identifier": identifier}, rath=rath
    ):
        yield event.reservations


def waiter(
    identifier: Optional[ID], rath: ArkitektRath = None
) -> Iterator[Optional[WaiterSubscriptionReservations]]:
    """waiter



    Arguments:
        identifier (ID): identifier
        rath (arkitekt.rath.ArkitektRath, optional): The arkitekt rath client

    Returns:
        WaiterSubscription"""
    for event in subscribe(WaiterSubscription, {"identifier": identifier}, rath=rath):
        yield event.reservations


async def atodolist(
    app_group: Optional[ID] = None, rath: ArkitektRath = None
) -> AssignationFragment:
    """todolist



    Arguments:
        app_group (Optional[ID], optional): appGroup.
        rath (arkitekt.rath.ArkitektRath, optional): The arkitekt rath client

    Returns:
        AssignationFragment"""
    return (await aexecute(TodolistQuery, {"appGroup": app_group}, rath=rath)).todolist


def todolist(
    app_group: Optional[ID] = None, rath: ArkitektRath = None
) -> AssignationFragment:
    """todolist



    Arguments:
        app_group (Optional[ID], optional): appGroup.
        rath (arkitekt.rath.ArkitektRath, optional): The arkitekt rath client

    Returns:
        AssignationFragment"""
    return execute(TodolistQuery, {"appGroup": app_group}, rath=rath).todolist


async def aget_provision(
    id: Optional[ID], rath: ArkitektRath = None
) -> Optional[Get_provisionQueryProvision]:
    """get_provision



    Arguments:
        id (ID): id
        rath (arkitekt.rath.ArkitektRath, optional): The arkitekt rath client

    Returns:
        Get_provisionQuery"""
    return (await aexecute(Get_provisionQuery, {"id": id}, rath=rath)).provision


def get_provision(
    id: Optional[ID], rath: ArkitektRath = None
) -> Optional[Get_provisionQueryProvision]:
    """get_provision



    Arguments:
        id (ID): id
        rath (arkitekt.rath.ArkitektRath, optional): The arkitekt rath client

    Returns:
        Get_provisionQuery"""
    return execute(Get_provisionQuery, {"id": id}, rath=rath).provision


async def aget_reservation(
    id: Optional[ID], rath: ArkitektRath = None
) -> Optional[Get_reservationQueryReservation]:
    """get_reservation



    Arguments:
        id (ID): id
        rath (arkitekt.rath.ArkitektRath, optional): The arkitekt rath client

    Returns:
        Get_reservationQuery"""
    return (await aexecute(Get_reservationQuery, {"id": id}, rath=rath)).reservation


def get_reservation(
    id: Optional[ID], rath: ArkitektRath = None
) -> Optional[Get_reservationQueryReservation]:
    """get_reservation



    Arguments:
        id (ID): id
        rath (arkitekt.rath.ArkitektRath, optional): The arkitekt rath client

    Returns:
        Get_reservationQuery"""
    return execute(Get_reservationQuery, {"id": id}, rath=rath).reservation


async def awaitlist(
    app_group: Optional[ID] = None, rath: ArkitektRath = None
) -> ReservationFragment:
    """waitlist



    Arguments:
        app_group (Optional[ID], optional): appGroup.
        rath (arkitekt.rath.ArkitektRath, optional): The arkitekt rath client

    Returns:
        ReservationFragment"""
    return (await aexecute(WaitlistQuery, {"appGroup": app_group}, rath=rath)).waitlist


def waitlist(
    app_group: Optional[ID] = None, rath: ArkitektRath = None
) -> ReservationFragment:
    """waitlist



    Arguments:
        app_group (Optional[ID], optional): appGroup.
        rath (arkitekt.rath.ArkitektRath, optional): The arkitekt rath client

    Returns:
        ReservationFragment"""
    return execute(WaitlistQuery, {"appGroup": app_group}, rath=rath).waitlist


async def afind(
    id: Optional[ID] = None,
    package: Optional[str] = None,
    interface: Optional[str] = None,
    template: Optional[ID] = None,
    q: Optional[QString] = None,
    rath: ArkitektRath = None,
) -> NodeFragment:
    """find

    Asss

        Is A query for all of these specials in the world


    Arguments:
        id (Optional[ID], optional): id.
        package (Optional[str], optional): package.
        interface (Optional[str], optional): interface.
        template (Optional[ID], optional): template.
        q (Optional[QString], optional): q.
        rath (arkitekt.rath.ArkitektRath, optional): The arkitekt rath client

    Returns:
        NodeFragment"""
    return (
        await aexecute(
            FindQuery,
            {
                "id": id,
                "package": package,
                "interface": interface,
                "template": template,
                "q": q,
            },
            rath=rath,
        )
    ).node


def find(
    id: Optional[ID] = None,
    package: Optional[str] = None,
    interface: Optional[str] = None,
    template: Optional[ID] = None,
    q: Optional[QString] = None,
    rath: ArkitektRath = None,
) -> NodeFragment:
    """find

    Asss

        Is A query for all of these specials in the world


    Arguments:
        id (Optional[ID], optional): id.
        package (Optional[str], optional): package.
        interface (Optional[str], optional): interface.
        template (Optional[ID], optional): template.
        q (Optional[QString], optional): q.
        rath (arkitekt.rath.ArkitektRath, optional): The arkitekt rath client

    Returns:
        NodeFragment"""
    return execute(
        FindQuery,
        {
            "id": id,
            "package": package,
            "interface": interface,
            "template": template,
            "q": q,
        },
        rath=rath,
    ).node


async def aget_template(
    id: Optional[ID], rath: ArkitektRath = None
) -> TemplateFragment:
    """get_template



    Arguments:
        id (ID): id
        rath (arkitekt.rath.ArkitektRath, optional): The arkitekt rath client

    Returns:
        TemplateFragment"""
    return (await aexecute(Get_templateQuery, {"id": id}, rath=rath)).template


def get_template(id: Optional[ID], rath: ArkitektRath = None) -> TemplateFragment:
    """get_template



    Arguments:
        id (ID): id
        rath (arkitekt.rath.ArkitektRath, optional): The arkitekt rath client

    Returns:
        TemplateFragment"""
    return execute(Get_templateQuery, {"id": id}, rath=rath).template


async def aget_agent(
    id: Optional[ID], rath: ArkitektRath = None
) -> Optional[Get_agentQueryAgent]:
    """get_agent



    Arguments:
        id (ID): id
        rath (arkitekt.rath.ArkitektRath, optional): The arkitekt rath client

    Returns:
        Get_agentQuery"""
    return (await aexecute(Get_agentQuery, {"id": id}, rath=rath)).agent


def get_agent(
    id: Optional[ID], rath: ArkitektRath = None
) -> Optional[Get_agentQueryAgent]:
    """get_agent



    Arguments:
        id (ID): id
        rath (arkitekt.rath.ArkitektRath, optional): The arkitekt rath client

    Returns:
        Get_agentQuery"""
    return execute(Get_agentQuery, {"id": id}, rath=rath).agent


async def aassign(
    reservation: Optional[ID],
    args: Optional[List[Optional[Dict]]],
    kwargs: Optional[Dict] = None,
    rath: ArkitektRath = None,
) -> AssignationFragment:
    """assign



    Arguments:
        reservation (ID): reservation
        args (List[Optional[Dict]]): args
        kwargs (Optional[Dict], optional): kwargs.
        rath (arkitekt.rath.ArkitektRath, optional): The arkitekt rath client

    Returns:
        AssignationFragment"""
    return (
        await aexecute(
            AssignMutation,
            {"reservation": reservation, "args": args, "kwargs": kwargs},
            rath=rath,
        )
    ).assign


def assign(
    reservation: Optional[ID],
    args: Optional[List[Optional[Dict]]],
    kwargs: Optional[Dict] = None,
    rath: ArkitektRath = None,
) -> AssignationFragment:
    """assign



    Arguments:
        reservation (ID): reservation
        args (List[Optional[Dict]]): args
        kwargs (Optional[Dict], optional): kwargs.
        rath (arkitekt.rath.ArkitektRath, optional): The arkitekt rath client

    Returns:
        AssignationFragment"""
    return execute(
        AssignMutation,
        {"reservation": reservation, "args": args, "kwargs": kwargs},
        rath=rath,
    ).assign


async def aunassign(
    assignation: Optional[ID], rath: ArkitektRath = None
) -> AssignationFragment:
    """unassign



    Arguments:
        assignation (ID): assignation
        rath (arkitekt.rath.ArkitektRath, optional): The arkitekt rath client

    Returns:
        AssignationFragment"""
    return (
        await aexecute(UnassignMutation, {"assignation": assignation}, rath=rath)
    ).unassign


def unassign(
    assignation: Optional[ID], rath: ArkitektRath = None
) -> AssignationFragment:
    """unassign



    Arguments:
        assignation (ID): assignation
        rath (arkitekt.rath.ArkitektRath, optional): The arkitekt rath client

    Returns:
        AssignationFragment"""
    return execute(UnassignMutation, {"assignation": assignation}, rath=rath).unassign


async def areserve(
    node: Optional[ID] = None,
    template: Optional[ID] = None,
    params: Optional[ReserveParamsInput] = None,
    title: Optional[str] = None,
    creator: Optional[ID] = None,
    app_group: Optional[ID] = None,
    rath: ArkitektRath = None,
) -> ReservationFragment:
    """reserve



    Arguments:
        node (Optional[ID], optional): node.
        template (Optional[ID], optional): template.
        params (Optional[ReserveParamsInput], optional): params.
        title (Optional[str], optional): title.
        creator (Optional[ID], optional): creator.
        app_group (Optional[ID], optional): appGroup.
        rath (arkitekt.rath.ArkitektRath, optional): The arkitekt rath client

    Returns:
        ReservationFragment"""
    return (
        await aexecute(
            ReserveMutation,
            {
                "node": node,
                "template": template,
                "params": params,
                "title": title,
                "creator": creator,
                "appGroup": app_group,
            },
            rath=rath,
        )
    ).reserve


def reserve(
    node: Optional[ID] = None,
    template: Optional[ID] = None,
    params: Optional[ReserveParamsInput] = None,
    title: Optional[str] = None,
    creator: Optional[ID] = None,
    app_group: Optional[ID] = None,
    rath: ArkitektRath = None,
) -> ReservationFragment:
    """reserve



    Arguments:
        node (Optional[ID], optional): node.
        template (Optional[ID], optional): template.
        params (Optional[ReserveParamsInput], optional): params.
        title (Optional[str], optional): title.
        creator (Optional[ID], optional): creator.
        app_group (Optional[ID], optional): appGroup.
        rath (arkitekt.rath.ArkitektRath, optional): The arkitekt rath client

    Returns:
        ReservationFragment"""
    return execute(
        ReserveMutation,
        {
            "node": node,
            "template": template,
            "params": params,
            "title": title,
            "creator": creator,
            "appGroup": app_group,
        },
        rath=rath,
    ).reserve


async def aunreserve(
    id: Optional[ID], rath: ArkitektRath = None
) -> ReservationFragment:
    """unreserve



    Arguments:
        id (ID): id
        rath (arkitekt.rath.ArkitektRath, optional): The arkitekt rath client

    Returns:
        ReservationFragment"""
    return (await aexecute(UnreserveMutation, {"id": id}, rath=rath)).unreserve


def unreserve(id: Optional[ID], rath: ArkitektRath = None) -> ReservationFragment:
    """unreserve



    Arguments:
        id (ID): id
        rath (arkitekt.rath.ArkitektRath, optional): The arkitekt rath client

    Returns:
        ReservationFragment"""
    return execute(UnreserveMutation, {"id": id}, rath=rath).unreserve


async def acreate_node(
    name: Optional[str],
    interface: Optional[str],
    args: Optional[List[Optional[ArgPortInput]]] = None,
    rath: ArkitektRath = None,
) -> NodeFragment:
    """create_node

    Create Node according to the specifications

    Arguments:
        name (str): name
        interface (str): interface
        args (Optional[List[Optional[ArgPortInput]]], optional): args.
        rath (arkitekt.rath.ArkitektRath, optional): The arkitekt rath client

    Returns:
        NodeFragment"""
    return (
        await aexecute(
            Create_nodeMutation,
            {"name": name, "interface": interface, "args": args},
            rath=rath,
        )
    ).create_node


def create_node(
    name: Optional[str],
    interface: Optional[str],
    args: Optional[List[Optional[ArgPortInput]]] = None,
    rath: ArkitektRath = None,
) -> NodeFragment:
    """create_node

    Create Node according to the specifications

    Arguments:
        name (str): name
        interface (str): interface
        args (Optional[List[Optional[ArgPortInput]]], optional): args.
        rath (arkitekt.rath.ArkitektRath, optional): The arkitekt rath client

    Returns:
        NodeFragment"""
    return execute(
        Create_nodeMutation,
        {"name": name, "interface": interface, "args": args},
        rath=rath,
    ).create_node


async def adefine(
    definition: Optional[DefinitionInput], rath: ArkitektRath = None
) -> NodeFragment:
    """define

    Defines a node according to is definition

    Arguments:
        definition (DefinitionInput): definition
        rath (arkitekt.rath.ArkitektRath, optional): The arkitekt rath client

    Returns:
        NodeFragment"""
    return (
        await aexecute(DefineMutation, {"definition": definition}, rath=rath)
    ).define


def define(
    definition: Optional[DefinitionInput], rath: ArkitektRath = None
) -> NodeFragment:
    """define

    Defines a node according to is definition

    Arguments:
        definition (DefinitionInput): definition
        rath (arkitekt.rath.ArkitektRath, optional): The arkitekt rath client

    Returns:
        NodeFragment"""
    return execute(DefineMutation, {"definition": definition}, rath=rath).define


async def areset_repository(
    rath: ArkitektRath = None,
) -> Optional[Reset_repositoryMutationResetrepository]:
    """reset_repository

    Create Repostiory

    Arguments:
        rath (arkitekt.rath.ArkitektRath, optional): The arkitekt rath client

    Returns:
        Optional[Reset_repositoryMutationResetrepository]"""
    return (await aexecute(Reset_repositoryMutation, {}, rath=rath)).reset_repository


def reset_repository(
    rath: ArkitektRath = None,
) -> Optional[Reset_repositoryMutationResetrepository]:
    """reset_repository

    Create Repostiory

    Arguments:
        rath (arkitekt.rath.ArkitektRath, optional): The arkitekt rath client

    Returns:
        Optional[Reset_repositoryMutationResetrepository]"""
    return execute(Reset_repositoryMutation, {}, rath=rath).reset_repository


async def acreate_template(
    node: Optional[ID],
    params: Optional[Dict] = None,
    extensions: Optional[List[Optional[str]]] = None,
    version: Optional[str] = None,
    rath: ArkitektRath = None,
) -> TemplateFragment:
    """create_template



    Arguments:
        node (ID): node
        params (Optional[Dict], optional): params.
        extensions (Optional[List[Optional[str]]], optional): extensions.
        version (Optional[str], optional): version.
        rath (arkitekt.rath.ArkitektRath, optional): The arkitekt rath client

    Returns:
        TemplateFragment"""
    return (
        await aexecute(
            Create_templateMutation,
            {
                "node": node,
                "params": params,
                "extensions": extensions,
                "version": version,
            },
            rath=rath,
        )
    ).create_template


def create_template(
    node: Optional[ID],
    params: Optional[Dict] = None,
    extensions: Optional[List[Optional[str]]] = None,
    version: Optional[str] = None,
    rath: ArkitektRath = None,
) -> TemplateFragment:
    """create_template



    Arguments:
        node (ID): node
        params (Optional[Dict], optional): params.
        extensions (Optional[List[Optional[str]]], optional): extensions.
        version (Optional[str], optional): version.
        rath (arkitekt.rath.ArkitektRath, optional): The arkitekt rath client

    Returns:
        TemplateFragment"""
    return execute(
        Create_templateMutation,
        {"node": node, "params": params, "extensions": extensions, "version": version},
        rath=rath,
    ).create_template


async def aslate(
    identifier: Optional[str], rath: ArkitektRath = None
) -> Optional[List[Optional[ID]]]:
    """slate



    Arguments:
        identifier (str): identifier
        rath (arkitekt.rath.ArkitektRath, optional): The arkitekt rath client

    Returns:
        Optional[List[Optional[ID]]]"""
    return (await aexecute(SlateMutation, {"identifier": identifier}, rath=rath)).slate


def slate(
    identifier: Optional[str], rath: ArkitektRath = None
) -> Optional[List[Optional[ID]]]:
    """slate



    Arguments:
        identifier (str): identifier
        rath (arkitekt.rath.ArkitektRath, optional): The arkitekt rath client

    Returns:
        Optional[List[Optional[ID]]]"""
    return execute(SlateMutation, {"identifier": identifier}, rath=rath).slate
