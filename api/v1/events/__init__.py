from fastapi import APIRouter

from .events import event_router

events_router = APIRouter()
events_router.include_router(event_router, tags=["Events"])

__all__ = ["events_router"]
