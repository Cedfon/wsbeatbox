from socketify import CompressOptions

from . import EndpointBaseBehavior

DEFAULT_BEHAVIOR: EndpointBaseBehavior = EndpointBaseBehavior({
    "compression": CompressOptions.DISABLED,
    "max_payload_length": 16 * 1024 * 1024,
    "idle_timeout": 0,
})