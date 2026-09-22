from typing import Literal
from pydantic import BaseModel, Field


class ConversationMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    conversation: list[ConversationMessage] = Field(default_factory=list)


class AvailableRoom(BaseModel):
    room_id: str
    name: str
    description: str
    max_guests: int
    price_per_night: float
    currency: str
    breakfast_included: bool
    beds: str


class AvailabilityData(BaseModel):
    available: bool
    check_in: str
    check_out: str
    guests: int
    rooms: list[AvailableRoom]


class ChatResponse(BaseModel):
    message: str
    type: Literal["answer", "availability", "error"]
    data: AvailabilityData | None = None