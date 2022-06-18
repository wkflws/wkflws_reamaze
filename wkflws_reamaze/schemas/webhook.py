from typing import Optional
from pydantic import BaseModel, Field


class ReamazeWebhook(BaseModel):
    to_number: dict = Field(alias="to")
    thread_id: Optional[str] = ""
    from_number: dict = Field(alias="from")
    conversation: dict
    body: str
    attachments: list = []
