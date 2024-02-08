from inspect import FullArgSpec
from socketify import CompressOptions, WebSocket, OpCode, Request, Response
from typing import TypedDict, Callable, Any, Optional
from enum import IntEnum


class EndpointBaseBehavior(TypedDict):
    compression: CompressOptions
    max_payload_length: int
    idle_timeout: int


class EndpointBehaviorHandlers(TypedDict):
    upgrade: Callable[[Response, Request, dict], None]
    open: Callable[[WebSocket], None]
    close: Callable[[WebSocket, int, str], None]
    message: Callable[[WebSocket, str, OpCode], None]
    drain: Callable[[WebSocket], None]
    subscription: Callable[[WebSocket, str, Any, Any], None]


class EndpointBehavior(EndpointBaseBehavior, EndpointBehaviorHandlers):
    pass


class EndpointControlItemDefinition(TypedDict):
    name: str
    func: Callable
    fullargspec: FullArgSpec
    doc: Optional[str]


class EndpointActionControl(EndpointControlItemDefinition):
    pass


class EndpointEventControl(EndpointControlItemDefinition):
    pass


class WebSocketMessageType(IntEnum):
    ACTION = 0
    EVENT = 1


class WebSocketBaseMessage(TypedDict):
    type: WebSocketMessageType
    message_id: Optional[str]
    data: Any
