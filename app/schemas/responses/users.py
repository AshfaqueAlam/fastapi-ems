from pydantic import UUID4, BaseModel, Field


class UserResponse(BaseModel):
    id: int = Field(..., example=1)
    uuid: UUID4 = Field(..., example="a3b8f042-1e16-4f0a-a8f0-421e16df0a2f")
    email: str = Field(..., example="john.doe@example.com")
    username: str = Field(..., example="john.doe")
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None
    check_in_status: bool | None = None

    class Config:
        orm_mode = True
