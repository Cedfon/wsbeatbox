import time
from socketify import App, WebSocket, Response, Request, AppListenOptions, AppOptions


from wsbeatbox.Endpoint import BasicEndpoint

app = App()
router = app.router()
test_endpoint = BasicEndpoint("/ws", app)


@test_endpoint.handlers.action("test")
def test():
    print("Test Action")


@router.get("/")
def index(response: Response, request: Request):
    print("Request", request)
    response.end(time.time())


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
