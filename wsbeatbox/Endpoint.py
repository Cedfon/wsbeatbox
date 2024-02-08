from socketify import App, CompressOptions, WebSocket, OpCode, Request, Response
from typing import Callable, Any, Dict, List

from .utils import format_endpoint_path, decode_incoming_message
from .interfaces import EndpointActionControl, EndpointBehavior, EndpointEventControl, WebSocketMessageType
from .constants import DEFAULT_BEHAVIOR
from .endpoint_handlers import EndpointHandlers


class BasicEndpoint:
    path: str
    app: App
    behavior: EndpointBehavior

    _handlers: EndpointHandlers = EndpointHandlers()
    sockets: Dict[str, WebSocket] = dict()

    def __init__(self, path: str, app: App, behavior: EndpointBehavior = DEFAULT_BEHAVIOR):
        self.path = format_endpoint_path(path)
        self.app = app
        self.behavior = behavior

        self.app.ws(path=self.path, behavior={
            "compression": self.behavior.get("compression", CompressOptions.DISABLED),
            "max_payload_length": self.behavior.get("max_payload_length", 16 * 1024 * 1024),
            "idle_timeout": self.behavior.get("idle_timeout", 0),
            "upgrade": self._on_upgrade,
            "open": self._on_open,
            "close": self._on_close,
            "message": self._on_message,
            "drain": self._on_drain,
            "subscription": self._on_subscription,
            "send_pings_automatically": True,
            "max_lifetime": 0,
            "close_on_backpressure_limit": False,
            "reset_idle_timeout_on_send": False,
            "max_backpressure": 64 * 1024,
        })

    @property
    def handlers(self) -> EndpointHandlers:
        return self._handlers

    def _on_upgrade(self, response: Response, request: Request, socket_context: dict):
        # Executing upgrade handlers
        for handler in self._handlers._upgrade_handlers:
            handler(response, request, socket_context)

        key = request.get_header("sec-websocket-key")
        extensions = request.get_header("sec-websocket-extensions")
        protocol = request.get_header("sec-websocket-protocol")
        # version = request.get_header("sec-websocket-version")

        user_data = {}

        # print(key, extensions, protocol, version, socket_context, user_data)

        response.upgrade(
            sec_web_socket_key=key,
            sec_web_socket_protocol=protocol,
            sec_web_socket_extensions=extensions,
            socket_context=socket_context,
            user_data=user_data,
        )

    def _on_open(self, ws: WebSocket):
        self.sockets.setdefault(ws.get_user_data_uuid(), ws)

        # Executing open handlers
        for handler in self._handlers._open_handlers:
            handler(ws)

    def _on_close(self, ws: WebSocket, code: int, reason: str):
        # print("Closed", ws, code, reason)
        self.sockets.pop(ws.get_user_data_uuid())

        # Executing close handlers
        for handler in self._handlers._close_handlers:
            handler(ws, code, reason)

    def _on_message(self, ws: WebSocket, message: str, opcode: OpCode):
        # print("Message", ws, message, opcode)

        # Executing message handlers
        for handler in self._handlers._message_handlers:
            handler(ws, message, opcode)

        try:
            message_json = decode_incoming_message(message, opcode)

            match message_json["type"]:
                case WebSocketMessageType.ACTION:
                    print("Action", message_json)
                    # Handling action
                case WebSocketMessageType.EVENT:
                    print("Event", message_json)
                    # Handling event
                case _:
                    raise ValueError(f"Invalid message type: {
                                     message_json['type']}")
        except Exception as err:
            print(err)

    def _on_drain(self, ws: WebSocket):
        # print("Drain", ws)

        # Executing drain handlers
        for handler in self._handlers._drain_handlers:
            handler(ws)

    def _on_subscription(self, ws: WebSocket, topic: str, subscriptions: Any, subscriptions_before: Any):
        # print("Subscription", ws, topic,
        #   subscriptions, subscriptions_before)

        # Executing subscription handlers
        for handler in self._handlers._subscription_handlers:
            handler(ws, topic, subscriptions, subscriptions_before)
