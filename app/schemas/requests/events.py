from pydantic import BaseModel

from datetime import datetime

class EventCreateRequest(BaseModel):
    name: str
    description: str
    start_time: datetime
    end_time: datetime
    location: str
    max_attendees: int


class EventUpdateRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    location: str | None = None
    max_attendees: int | None = None
