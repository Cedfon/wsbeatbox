# wsbeatbox
> "Two drums & two sticks I'm beatboxin'"

Server side helpers for WebSocket build on top of `socketify`.

## Use cases

```py
test_endpoint = Endpoint("/test", {
  # ...
})

@test_endpoint.action("foo")
def foo(a: int):
  print("Foo", a)

@test_endpoint.event("bar")
def bar(b: int):
  print("Bar", a)
```
