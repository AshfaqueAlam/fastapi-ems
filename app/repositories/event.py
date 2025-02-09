from sqlalchemy import Select
from sqlalchemy.sql.expression import select

# from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy.orm import joinedload

from app.models import Event, User
from core.database import Propagation, Transactional
from core.repository import BaseRepository


class EventRepository(BaseRepository[Event]):
    """
    Event repository provides all the database operations for the Event model.
    """

    async def get_by_id(
        self, event_id: int, join_: set[str] | None = None
    ) -> Event | None:
        """
        Get event by ID.

        :param event_id: Event ID.
        :param join_: Join relations.
        :return: Event.
        """
        query = self._query(join_)
        query = query.filter(Event.event_id == event_id)

        if join_ is not None:
            return await self.all_unique(query)

        return await self._one_or_none(query)

    async def get_by_name(
        self, name: str, join_: set[str] | None = None
    ) -> Event | None:
        """
        Get event by name.

        :param name: Event name.
        :param join_: Join relations.
        :return: Event.
        """
        query = self._query(join_)
        query = query.filter(Event.name == name)

        if join_ is not None:
            return await self.all_unique(query)

        return await self._one_or_none(query)

    @Transactional(propagation=Propagation.REQUIRED)
    async def create_event(self, event_data: dict) -> Event:
        """
        Create a new event.

        :param event_data: Data for the new event.
        :return: Created event.
        """
        
        return await self.create(event_data)
        # event = Event(**event_data.dict())
        # self.session.add(event)
        # await self.session.commit()
        # await self.session.refresh(event)
        # return event

    @Transactional(propagation=Propagation.REQUIRED)
    async def update_event(self, event_id: int, event_data: dict) -> Event | None:
        """
        Update an existing event.

        :param event_id: Event ID.
        :param event_data: Data to update the event.
        :return: Updated event.
        """
        event = await self.get_by_id(event_id)
        if event:
            for key, value in event_data.items():
                print("key: ", key, "value: ", value)
                setattr(event, key, value)
            # await self.session.commit()
            # await self.session.refresh(event)
        return event

    async def delete_event(self, event_id: int) -> bool:
        """
        Delete an event.

        :param event_id: Event ID.
        :return: True if the event was deleted, False otherwise.
        """
        event = await self.get_by_id(event_id)
        if event:
            await self.session.delete(event)
            await self.session.commit()
            return True
        return False

    async def is_attendee_limit_reached(self, event_id: int) -> bool:
        """
        Check if the max_attendees limit for the event has been reached.

        :param event_id: Event ID.
        :return: True if the limit is reached, False otherwise.
        """
        event = await self.get_by_id(event_id)
        if not event:
            raise ValueError(f"Event with ID {event_id} not found")

        attendee_count = await self.session.scalar(
            select(func.count(User.id)).where(User.event_id == event_id)
        )

        return attendee_count >= event.max_attendees
