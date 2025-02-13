from pydantic import EmailStr

from app.models import User
from app.repositories import UserRepository, EventRepository
from app.schemas.extras.token import Token
from app.schemas.requests.users import RegisterUserRequest
from core.controller import BaseController
from core.database import Propagation, Transactional
from core.exceptions import BadRequestException, UnauthorizedException
from core.security import JWTHandler, PasswordHandler


class AuthController(BaseController[User]):
    def __init__(self, user_repository: UserRepository, event_repository: EventRepository):
        super().__init__(model=User, repository=user_repository)
        self.user_repository = user_repository
        self.event_repository = event_repository

    @Transactional(propagation=Propagation.REQUIRED)
    async def register(
        self, request_data: RegisterUserRequest
    ) -> User:  # email: EmailStr, password: str, username: str
        # Check if user exists with email
        user = await self.user_repository.get_by_email(request_data.email)

        if user:
            raise BadRequestException("User already exists with this email")

        # Check if user exists with username
        user = await self.user_repository.get_by_username(request_data.username)

        if user:
            raise BadRequestException("User already exists with this username")

        if await self.event_repository.is_attendee_limit_reached(request_data.event_id):
            raise BadRequestException("Event is full. Registration closed for this event.")

        # Hash the password
        hashed_password = PasswordHandler.hash(request_data.password)
        request_data.password = hashed_password

        return await self.user_repository.create(
            # {
            #     "email": email,
            #     "password": password,
            #     "username": username,
            # }
            request_data.dict()
        )

    async def login(self, email: EmailStr, password: str) -> Token:
        user = await self.user_repository.get_by_email(email)

        if not user:
            raise BadRequestException("Invalid credentials")

        if not PasswordHandler.verify(user.password, password):
            raise BadRequestException("Invalid credentials")

        return Token(
            access_token=JWTHandler.encode(payload={"user_id": user.id}),
            refresh_token=JWTHandler.encode(payload={"sub": "refresh_token"}),
        )

    async def refresh_token(self, access_token: str, refresh_token: str) -> Token:
        token = JWTHandler.decode(access_token)
        refresh_token = JWTHandler.decode(refresh_token)
        if refresh_token.get("sub") != "refresh_token":
            raise UnauthorizedException("Invalid refresh token")

        return Token(
            access_token=JWTHandler.encode(payload={"user_id": token.get("user_id")}),
            refresh_token=JWTHandler.encode(payload={"sub": "refresh_token"}),
        )
