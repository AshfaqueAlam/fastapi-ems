> python main.py
---
> alembic revision --autogenerate -m "$$message"
> alembic upgrade head


### Project Structure Overview
1. **api/**: Contains the API routers.
2. **app/**: Contains the application-specific logic.
    * **controllers/**: Contains the business logic, similar to Django's views.
    * **models/**: Contains the database models, similar to Django's models.
    * **repositories/**: Contains the data access layer, responsible for querying the database.
    * **schemas/**: Contains the Pydantic models for request and response validation, similar to Django's serializers.
3. **core/**: Contains the core components and configurations used across the application.

### Detailed Explanation
* **Controllers:** These are responsible for handling the business logic. They interact with repositories to fetch or manipulate data and return the results.
* **Repositories:** These are responsible for interacting with the database. They contain methods for querying the database and returning the results.
* **Schemas:** These are Pydantic models used for request validation and response serialization. They ensure that the data conforms to the expected structure.

