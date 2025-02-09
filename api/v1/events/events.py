from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.controllers import EventController
from app.schemas.requests.events import EventCreateRequest, EventUpdateRequest
from app.schemas.responses.events import EventResponse
from core.factory import Factory
from core.fastapi.dependencies import AuthenticationRequired


event_router = APIRouter()


@event_router.post(
    "/",
    dependencies=[Depends(AuthenticationRequired)],
    # response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_event(
    request_data: EventCreateRequest,
    event_controller: EventController = Depends(Factory().get_event_controller),
) -> EventResponse:
    return await event_controller.create_event(request_data)


@event_router.put(
    "/{event_id}",
    dependencies=[Depends(AuthenticationRequired)],
    response_model=EventResponse,
)
async def update_event(
    event_id: int,
    request_data: EventUpdateRequest,
    event_controller: EventController = Depends(Factory().get_event_controller),
) -> EventResponse:
    return await event_controller.update_event(event_id, request_data)


@event_router.get(
    "/{event_id}",
    dependencies=[Depends(AuthenticationRequired)],
    response_model=EventResponse,
)
async def get_event(
    event_id: int,
    event_controller: EventController = Depends(Factory().get_event_controller),
) -> EventResponse:
    event = event_controller.get_event(event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
        )
    return await event


@event_router.get(
    "/",
    dependencies=[Depends(AuthenticationRequired)],
    response_model=list[EventResponse],
)
async def list_events(
    event_controller: EventController = Depends(Factory().get_event_controller),
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = Query(None, description="Filter by event status"),
    location: Optional[str] = Query(None, description="Filter by event location"),
    start_date: Optional[datetime] = Query(None, description="Filter by start date"),
    end_date: Optional[datetime] = Query(None, description="Filter by end date"),
) -> List[EventResponse]:
    filters = {}
    if status:
        filters["status"] = status
    if location:
        filters["location"] = location
    return await event_controller.get_all(skip=skip, limit=limit, filters=filters)
