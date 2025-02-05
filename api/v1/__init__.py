from fastapi import APIRouter

from .monitoring import monitoring_router
from .users import user_router
# from .event import event_router

v1_router = APIRouter()
v1_router.include_router(monitoring_router, prefix="/monitoring")
v1_router.include_router(user_router, prefix="/users")
# v1_router.include_router(event_router, prefix="/event")
