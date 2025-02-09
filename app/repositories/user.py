from sqlalchemy import Select
# from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.models import User
from core.repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    User repository provides all the database operations for the User model.
    """

    async def get_by_username(
        self, username: str, join_: set[str] | None = None
    ) -> User | None:
        """
        Get user by username.

        :param username: Username.
        :param join_: Join relations.
        :return: User.
        """
        query = self._query(join_)
        query = query.filter(User.username == username)

        if join_ is not None:
            return await self.all_unique(query)

        return await self._one_or_none(query)

    async def get_by_email(
        self, email: str, join_: set[str] | None = None
    ) -> User | None:
        """
        Get user by email.

        :param email: Email.
        :param join_: Join relations.
        :return: User.
        """
        query = self._query(join_)
        query = query.filter(User.email == email)

        if join_ is not None:
            return await self.all_unique(query)

        return await self._one_or_none(query)

    # def _join_tasks(self, query: Select) -> Select:
    #     """
    #     Join tasks.

    #     :param query: Query.
    #     :return: Query.
    #     """
    #     return query.options(joinedload(User.tasks)).execution_options(
    #         contains_joined_collection=True
    #     )


'''
This file is part of the repository layer in your FastAPI project. The repository pattern is used to separate the data access logic from the business logic. This makes your code more modular, easier to maintain, and test.

### Structure of user.py

1. **Methods for Querying Users**:
    - `get_by_username`: Fetches a user by their username.
    - `get_by_email`: Fetches a user by their email address.

2. **Helper Methods**:
    - `_query`: Constructs the base query for the `User` model.
    - `_one_or_none`: Executes the query and returns one or no result.
    - `all_unique`: Executes the query and returns all unique results.
    - `_join_tasks`: Joins the `tasks` relationship to the user query.

### `_join_tasks` Method

#### Purpose

The `_join_tasks` method is used to join the `tasks` relationship to the user query. This is useful when you want to fetch a user along with their associated tasks in a single query. This can improve performance by reducing the number of database round-trips.

#### Implementation

```python
def _join_tasks(self, query: Select) -> Select:
    """
    Join tasks.

    :param query: Query.
    :return: Query.
    """
    return query.options(joinedload(User.tasks)).execution_options(
        contains_joined_collection=True
    )
```

#### Explanation

- **Parameter**: The method takes a `query` parameter, which is an SQLAlchemy `Select` object representing the base query for the `User` model.
- **joinedload**: This function is used to specify that the `tasks` relationship should be eagerly loaded. This means that when the user is fetched, their associated tasks will be loaded in the same query.
- **execution_options**: The `contains_joined_collection=True` option is used to optimize the query execution when a joined collection is present.

### Why This Method is There The `_join_tasks` method solves the problem of efficiently loading related data. In this case, it allows you to fetch a user along with their tasks in a single query, which can be more efficient than fetching the user and then separately fetching their tasks.

### Example Usage

Here's an example of how `_join_tasks` might be used in a method that fetches users with their tasks:

```python
async def get_user_with_tasks(self, user_id: int) -> User | None:
    query = self._query().filter(User.id == user_id)
    query = self._join_tasks(query)
    return await self._one_or_none(query)
```

In this example, the `get_user_with_tasks` method constructs a query to fetch a user by their ID and then uses `_join_tasks` to ensure that the user's tasks are also loaded in the same query.

### Summary

- **Purpose**: `user.py` is part of the repository layer, providing methods to query the `User` model.
- **Structure**: It contains methods for querying users and helper methods for constructing and executing queries.
- **_join_tasks**: This method is used to join the `tasks` relationship to the user query, allowing for efficient loading of related data.

This structure and approach help in maintaining clean, modular, and efficient data access logic in your FastAPI project.
'''
