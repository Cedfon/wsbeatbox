import inspect
from inspect import FullArgSpec, get_annotations
import time
import json
from typing import TypedDict, Callable
from socketify import App, WebSocket, Response, Request, AppListenOptions, AppOptions


from wsbeatbox import BasicEndpoint

app = App()
router = app.router()
test_endpoint = BasicEndpoint("/ws", app)


class TestType(TypedDict):
    a: int
    b: str
    c: dict

@test_endpoint.handlers.action("test")
def test(obj: TestType):
    """This is the doc for the `test` action"""
    print("Test Action", obj)


@router.get("/introspect")
def index(response: Response, request: Request):
    """
    Testing ws endpoint introspection functionality.
    
    go to: http://{SERVER_HOST}/introspect
    """
    
    # Gettin' the `fullargspec` and `doc` properties of the declared action instance and then converting it to a list of dictionaries to be serialized to JSON
    results = list(map(lambda value: dict(
        doc=value["doc"], fullargspec=value["fullargspec"]), test_endpoint.handlers._actions.values()))

    json_dict = dict.fromkeys(test_endpoint.handlers._actions.keys(), results)

    response.write(json.dumps(json_dict))
    response.end("")


@test_endpoint.handlers.open()
def custom_on_open(ws: WebSocket):
    print("Custom On Open", ws.get_user_data_uuid())


@test_endpoint.handlers.open()
def custom_on_open2(ws: WebSocket):
    print("Custom On Open 2")


@test_endpoint.handlers.open()
def custom_on_open3(ws: WebSocket):
    print("Custom On Open 3")


@test_endpoint.handlers.open()
def custom_on_open4(ws: WebSocket):
    print("Custom On Open 4")


@router.get("/count")
def count(response: Response, request: Request):

    response.end(len(app._socket_refs))

    print(len(test_endpoint.sockets))
    for socket in test_endpoint.sockets.values():
        socket.send(f"{time.time()}")


def listener_handler(info: AppOptions):
    print(f"Listening on {info.host}:{info.port}")


if __name__ == "__main__":
    app.listen(
        port_or_options=AppListenOptions(port=8080, host="10.0.0.38"),
        handler=listener_handler,
    )

    app.run()
