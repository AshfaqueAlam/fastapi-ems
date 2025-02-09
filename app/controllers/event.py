from app.models import Event
from app.repositories import EventRepository
from app.schemas.requests.events import EventCreateRequest, EventUpdateRequest
from core.controller import BaseController


class EventController(BaseController[Event]):
    def __init__(self, event_repository: EventRepository):
        super().__init__(model=Event, repository=event_repository)
        self.event_repository = event_repository

    async def create_event(self, request_data: EventCreateRequest) -> Event:
        return await self.event_repository.create_event(request_data.dict())

    async def update_event(self, event_id: int, request_data: EventUpdateRequest) -> Event:
        return await self.event_repository.update_event(event_id, request_data.dict())

    async def get_event(self, event_id: int) -> Event:
        return await self.event_repository.get_by_id(event_id)
