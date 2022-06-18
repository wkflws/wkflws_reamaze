from typing import Any, Optional

import json
from wsgiref import validate

from wkflws.events import Event
from wkflws.http import http_method, Request, Response
from wkflws.logging import getLogger
from wkflws.triggers.webhook import WebhookTrigger

from . import __identifier__, __version__
from .schemas.webhook import ReamazeWebhook

logger = getLogger("wkflws_reamaze.trigger")
logger.setLevel(10)


async def process_webhook_request(
    request: Request, response: Response
) -> Optional[Event]:
    """Accept and process an HTTP request returning a event for the bus."""

    try:
        identifier = request.headers["x-reamaze-hmac-sha256"]
    except KeyError:
        raise ValueError("'x-reamaze-hmac-sha256' undefined!") from None

    data = json.loads(request.body)
    reamaze_webhook = ReamazeWebhook(**data).dict(by_alias=True)
    request.headers["from_phone"] = data.get("from").get("phone")
    print(request.headers)
    logger.info(f"Received Reamaze webhook request: {identifier}")

    return Event(identifier, request.headers, reamaze_webhook)


async def accept_event(event: Event) -> tuple[Optional[str], dict[str, Any]]:
    """Accept and process data from the event bus."""
    logger.info(f"Processing Reamaze webhook'")

    return "wkflws_reamaze.outbound", event.data


my_webhook_trigger = WebhookTrigger(
    client_identifier=__identifier__,
    client_version=__version__,
    process_func=accept_event,
    routes=(
        (
            (http_method.POST,),
            "/webhook/",
            process_webhook_request,
        ),
    ),
)
