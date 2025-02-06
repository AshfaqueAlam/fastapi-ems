from enum import Enum
from uuid import uuid4

from sqlalchemy import BigInteger, Column, Unicode
from sqlalchemy.dialects.postgresql import UUID

from core.database import Base
from core.database.mixins import TimestampMixin


class EventStatus(Enum):
    SCHEDULED = "scheduled"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Event(Base, TimestampMixin):
    __tablename__ = "events"

    event_id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(Unicode(255), nullable=False)
    description = Column(Unicode(255), nullable=True)
    # start_time: DateTime
    # end_time: DateTime
    location = Column(Unicode(255), nullable=True)
    # max_attendees: Integer
    # status: Enum('scheduled', 'ongoing', 'completed', 'cancelled')

    __mapper_args__ = {"eager_defaults": True}
