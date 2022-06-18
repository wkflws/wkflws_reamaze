import hmac
import hashlib
import base64


def create_sha256_signature(secret, message):
    message = bytes(message, "utf-8")
    secret = bytes(secret, "utf-8")

    signature = base64.b64encode(
        hmac.new(secret, message, digestmod=hashlib.sha256).digest()
    )
    return signature.decode("utf-8")


def validate_payload(payload: str, shared_secret: str, reamaze_hmac: str) -> bool:
    """Validate the payload."""

    # remove whitespaces
    payload = payload.replace(": ", ":").replace(", ", ",")
    signature = create_sha256_signature(
        shared_secret,
        payload,
    )

    if signature == reamaze_hmac:
        return True

    return False
