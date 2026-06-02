from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    email: EmailStr
    role: str = Field(default="user", min_length=2, max_length=40)


class UserResponse(UserCreate):
    id: int
    is_active: bool = True
