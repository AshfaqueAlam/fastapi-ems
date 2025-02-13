from typing import Callable, List, Optional

from fastapi import APIRouter, Depends, File, Query, UploadFile

from app.controllers import AuthController, UserController, EventController
from app.models.user import User, UserPermission
from app.schemas.extras.token import Token
from app.schemas.requests.users import LoginUserRequest, RegisterUserRequest
from app.schemas.responses.users import UserResponse
from core.factory import Factory
from core.fastapi.dependencies import AuthenticationRequired
from core.fastapi.dependencies.current_user import get_current_user
from core.fastapi.dependencies.permissions import Permissions

user_router = APIRouter()


@user_router.get("/", dependencies=[Depends(AuthenticationRequired)])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    user_controller: UserController = Depends(Factory().get_user_controller),
    assert_access: Callable = Depends(Permissions(UserPermission.READ)),
    event_id: Optional[int] = Query(None, description="Filter by event ID"),
) -> list[UserResponse]:

    filters: dict[str, int] = {}
    if event_id:
        filters["event_id"] = event_id

    users = await user_controller.get_all(skip=skip, limit=limit, filters=filters)

    assert_access(resource=users)
    return users


@user_router.post("/", status_code=201)
async def register_user(
    register_user_request: RegisterUserRequest,
    auth_controller: AuthController = Depends(Factory().get_auth_controller),
) -> UserResponse:
    return await auth_controller.register(
        # email=register_user_request.email,
        # password=register_user_request.password,
        # username=register_user_request.username,
        register_user_request
    )


@user_router.post("/login")
async def login_user(
    login_user_request: LoginUserRequest,
    auth_controller: AuthController = Depends(Factory().get_auth_controller),
) -> Token:
    return await auth_controller.login(
        email=login_user_request.email, password=login_user_request.password
    )


@user_router.get("/me", dependencies=[Depends(AuthenticationRequired)])
def get_user(
    user: User = Depends(get_current_user),
) -> UserResponse:
    return user


@user_router.put("/checkin", dependencies=[Depends(AuthenticationRequired)])
async def checkin_user(
    user_controller: UserController = Depends(Factory().get_user_controller),
    user: User = Depends(get_current_user),
) -> UserResponse:
    return await user_controller.checkin(user)


@user_router.post("/bulk_checkin", dependencies=[Depends(AuthenticationRequired)])
async def bulk_checkin(
    user_controller: UserController = Depends(Factory().get_user_controller),
    file: UploadFile = File(...),
) -> List[UserResponse]:
    return await user_controller.bulk_checkin(file)
