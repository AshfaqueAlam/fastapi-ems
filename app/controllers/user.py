import csv
import io
from typing import List

from fastapi import UploadFile

from app.models import User
from app.repositories import UserRepository
from core.controller import BaseController
from core.exceptions import BadRequestException


class UserController(BaseController[User]):
    def __init__(self, user_repository: UserRepository):
        super().__init__(model=User, repository=user_repository)
        self.user_repository = user_repository

    async def get_by_username(self, username: str) -> User:
        return await self.user_repository.get_by_username(username)

    async def get_by_email(self, email: str) -> User:
        return await self.user_repository.get_by_email(email)

    async def checkin(self, user: User) -> User:
        return await self.user_repository.checkin(user)

    async def bulk_checkin(self, file: UploadFile) -> List[User]:
        if not file.filename.endswith(".csv"):
            raise BadRequestException("Only CSV files are allowed.")

        content = await file.read()
        content = content.decode("utf-8")
        csv_reader = csv.reader(io.StringIO(content))
        header = next(csv_reader, None)
        if not header:
            raise BadRequestException("Invalid CSV format: Missing headers.")

        data = []
        for row in csv_reader:
            data.append(dict(zip(header, row)))

        return await self.user_repository.bulk_checkin(data)
