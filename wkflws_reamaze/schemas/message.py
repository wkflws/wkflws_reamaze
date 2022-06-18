from uuid import uuid4
from typing import Optional
from pydantic import BaseModel, Field


class ReamazeMessage(BaseModel):
    id: Optional[str] = str(uuid4())
    direction: Optional[str] = "inbound"
    to_number: dict = Field(alias="to")
    from_number: dict = Field(alias="from")
    body: str
    thread_id: Optional[str] = ""
