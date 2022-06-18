import json
import sys

import requests
from typing import Any
from .utils import create_sha256_signature
from .schemas.message import ReamazeMessage

from wkflws.logging import getLogger

from . import __identifier__, __version__

logger = getLogger("wkflws_reamaze.send_message")
logger.setLevel(10)


async def send_message(
    message: dict[str, Any], context: dict[str, Any]
) -> dict[str, Any]:

    try:
        reamaze_token = context["Task"]["reamaze_shared_secret"]
    except KeyError:
        raise ValueError(
            "Context value `reamaze_shared_secret` was not provided in the context. Unable "
            "to proceed."
        ) from None

    message["to"] = {"phone": message["to"]}
    message["from"] = {"phone": message["from"]}
    payload = json.dumps(ReamazeMessage(**message).dict(by_alias=True))

    signature = create_sha256_signature(reamaze_token, payload)
    headers = {
        "Content-Type": "application/json",
        "X-Reamaze-Hmac-SHA256": signature,
    }

    response = requests.post(
        "https://www.reamaze.io/incoming/sms", data=payload, headers=headers
    )

    if response.status_code != 200:
        logger.error(
            f"Reamaze webhook request failed with status code {response.status_code}"
        )

    return message


if __name__ == "__main__":
    import asyncio
    import sys

    try:
        message = json.loads(sys.argv[1])
    except IndexError:
        raise ValueError("missing required `message` argument") from None

    try:
        context = json.loads(sys.argv[2])
    except IndexError:
        raise ValueError("missing `context` argument") from None

    output = asyncio.run(send_message(message, context))

    if output is None:
        sys.exit(1)

    print(json.dumps(output))
