from inspect import FullArgSpec
import inspect
import json
from typing import Callable, Any, Dict, List
from socketify import WebSocket, OpCode, Request, Response

from .utils import traverse_annotations

from .interfaces import EndpointActionControl, EndpointEventControl


def jsonify_fullargspec(fullargspec: FullArgSpec) -> Dict:
    """
    Convert FullArgSpec to JSON parsable dictionary
    """

    annotations_dict = {}

    for (key, value) in fullargspec.annotations.items():
        annotations_dict.setdefault(key, value.__name__)

    return {
        "args": fullargspec.args,
        "varargs": fullargspec.varargs,
        "varkw": fullargspec.varkw,
        "defaults": fullargspec.defaults,
        "kwonlyargs": fullargspec.kwonlyargs,
        "kwonlydefaults": fullargspec.kwonlydefaults,
        "annotations": annotations_dict
    }


class EndpointHandlers:
    _upgrade_handlers: List[Callable[[Response, Request, dict], None]] = []
    _open_handlers: List[Callable[[WebSocket], None]] = []
    _close_handlers: List[Callable[[WebSocket, int, str], None]] = []
    _message_handlers: List[Callable[[WebSocket, str, OpCode], None]] = []
    _drain_handlers: List[Callable[[WebSocket], None]] = []
    _subscription_handlers: List[Callable[[
        WebSocket, str, Any, Any], None]] = []

    _actions: Dict[str, EndpointActionControl] = dict()
    _events: Dict[str, EndpointEventControl] = dict()

    def action(self, action_name: str = None) -> Callable:
        # print("Inside Action", action_name)

        def decorator(func: Callable):
            # print("Inside Decorator", action_name)

            _action_name = action_name or func.__name__
            fullargspec = inspect.getfullargspec(func)
            fullargspec_dict = jsonify_fullargspec(fullargspec)
            doc = inspect.getdoc(func)

            print(inspect.get_annotations(func))
            for (key, value) in inspect.get_annotations(func).items():
                print(key, value.__name__)

                # If not an object of primitive, then traverse the type and get the type name
                print("B", traverse_annotations(inspect.get_annotations(value)))

            def wrapper(*args, **kwargs):
                print("Inside Wrapper", action_name)
                print(inspect.signature(func))

                func_result = func(*args, **kwargs)
                return func_result

            wrapper({})
            self._actions.setdefault(_action_name, {
                "name": _action_name,
                "func": wrapper,
                "fullargspec": traverse_annotations(inspect.get_annotations(value)),
                "doc": doc or "",
            })

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
