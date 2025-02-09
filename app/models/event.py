from enum import Enum
from uuid import uuid4

from sqlalchemy import BigInteger, Column, Unicode, DateTime, Integer, Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core.database import Base
from core.database.mixins import TimestampMixin


class EventStatus(str, Enum):
    SCHEDULED = "scheduled"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Event(Base, TimestampMixin):
    __tablename__ = "events"

    event_id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(Unicode(255), nullable=False)
    description = Column(Unicode(255), nullable=True)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    location = Column(Unicode(255), nullable=True)
    max_attendees = Column(Integer, nullable=False)
    status = Column(SQLAlchemyEnum(EventStatus), nullable=False, default=EventStatus.SCHEDULED)

    # Define the users relationship
    users = relationship("User", back_populates="event")

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return f"<Event(event_id={self.event_id}, name={self.name}, status={self.status})>"
