from pydantic import BaseModel

from datetime import datetime


class EventResponse(BaseModel):
    event_id: int
    name: str
    description: str
    start_time: datetime
    end_time: datetime
    location: str
    max_attendees: int
    created_at: datetime
    updated_at: datetime
    status: str

    class Config:
        orm_mode = True
