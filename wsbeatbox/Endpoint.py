from socketify import App, CompressOptions, WebSocket, OpCode, Request, Response
from typing import Callable, Any, Dict, List

from . import format_endpoint_path, EndpointActionControl, EndpointBehavior, EndpointEventControl, DEFAULT_BEHAVIOR, WebSocketBaseMessage, WebSocketMessageType, decode_incoming_message


class EndpointHandlers:
    _upgrade_handlers: List[Callable[[Response, Request, dict], None]] = []
    _open_handlers: List[Callable[[WebSocket], None]] = []
    _close_handlers: List[Callable[[WebSocket, int, str], None]] = []
    _message_handlers: List[Callable[[WebSocket, str, OpCode], None]] = []
    _drain_handlers: List[Callable[[WebSocket], None]] = []
    _subscription_handlers: List[Callable[[
        WebSocket, str, Any, Any], None]] = []

    _actions: Dict[str, EndpointActionControl]
    _events: Dict[str, EndpointEventControl]

    def action(self, action_name: str) -> Callable:
        # print("Inside Action", action_name)

        def decorator(func: Callable):
            # print("Inside Decorator", action_name)

            def wrapper(*args, **kwargs):
                # print("Inside Wrapper", action_name)

                func_result = func(*args, **kwargs)
                return func_result

            return wrapper

        return decorator

    def upgrade(self):
        def decorator(func: Callable):
            self._upgrade_handlers.append(func)

            def wrapper(*args, **kwargs):
                func_result = func(*args, **kwargs)
                return func_result

            return wrapper

        return decorator

    def open(self):
        def decorator(func: Callable):
            self._open_handlers.append(func)

            def wrapper(*args, **kwargs):
                func_result = func(*args, **kwargs)
                return func_result

            return wrapper

        return decorator

    def close(self):
        def decorator(func: Callable):
            self._close_handlers.append(func)

            def wrapper(*args, **kwargs):
                func_result = func(*args, **kwargs)
                return func_result

            return wrapper

        return decorator

    def message(self):
        def decorator(func: Callable):
            self._message_handlers.append(func)

            def wrapper(*args, **kwargs):
                func_result = func(*args, **kwargs)
                return func_result

            return wrapper

        return decorator

    def drain(self):
        def decorator(func: Callable):
            self._drain_handlers.append(func)

            def wrapper(*args, **kwargs):
                func_result = func(*args, **kwargs)
                return func_result

            return wrapper

        return decorator

    def subscription(self):
        def decorator(func: Callable):
            self._subscription_handlers.append(func)

            def wrapper(*args, **kwargs):
                func_result = func(*args, **kwargs)
                return func_result

            return wrapper

        return decorator


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

        self.app.ws("/ws", behavior={
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
