from functools import partial

from fastapi import Depends

from app.controllers import AuthController, UserController, EventController  # TaskController
from app.models import User, Event  # Task
from app.repositories import UserRepository, EventRepository  # TaskRepository
from core.database import get_session


class Factory:
    """
    This is the factory container that will instantiate all the controllers and
    repositories which can be accessed by the rest of the application.
    """

    # Repositories
    # task_repository = partial(TaskRepository, Task)
    user_repository = partial(UserRepository, User)
    event_repository = partial(EventRepository, Event)

    def get_user_controller(self, db_session=Depends(get_session)):
        return UserController(
            user_repository=self.user_repository(db_session=db_session)
        )

    # def get_task_controller(self, db_session=Depends(get_session)):
    #     return TaskController(
    #         task_repository=self.task_repository(db_session=db_session)
    #     )

    def get_auth_controller(self, db_session=Depends(get_session)):
        return AuthController(
            user_repository=self.user_repository(db_session=db_session),
            event_repository=self.event_repository(db_session=db_session),  # For event registration full validation...
        )

    def get_event_controller(self, db_session=Depends(get_session)):
        return EventController(
            event_repository=self.event_repository(db_session=db_session),
        )
