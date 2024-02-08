from socketify import OpCode
import re
import json

from .interfaces import WebSocketMessageType


def format_endpoint_path(path: str):
    # Validate and format an endpoint path.
    # Endpoint path can be define such as `./some/path`, `some/path`, `\some\path`, `some\path`, `some/path/`, ...etc
    # This function will format the path to be a valid endpoint path in the format `some/path`

    # Remove leading and trailing whitespaces
    path = path.strip()

    # Replace backslashes with forward slashes
    path = path.replace('\\', '/')

    # Remove leading dot and slash
    path = re.sub(r'^[./]+', '', path)

    # Remove trailing slash
    path = re.sub(r'/$', '', path)

    # Check if the path is empty
    if not path:
        raise ValueError("Endpoint path cannot be empty")

    # Check if the path contains any invalid characters
    if not re.match(r'^[a-zA-Z0-9_/]+$', path):
        raise ValueError("Endpoint path contains invalid characters")

    return path


def decode_incoming_message(message: str, opcode: OpCode):
    message_json = None

    try:
        match opcode:
            case OpCode.TEXT:
                message_json = json.loads(message)
            case OpCode.BINARY:
                decoded_message = message.decode("utf-8")
                message_json = json.loads(decoded_message)

            case _:
                raise ValueError(f"Invalid opcode: {opcode}")

    except Exception as err:
        raise err
    finally:
        if message_json is None:
            raise ValueError("Invalid message format")

        if "type" not in message_json:
            raise ValueError(
                "No type was specified in the incoming message")

        if "type" in message_json and message_json["type"] == WebSocketMessageType.ACTION and "message_id" not in message_json:
            raise ValueError(
                "Action message received without an identifier")

        return message_json
