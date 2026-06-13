from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr


class UserRegister(BaseModel):
    first_name: str = Field(..., description="Enter your first name.")
    last_name: str = Field(..., description="Enter your second name.")
    patronymic: str | None = Field(..., description="Enter your patronymic.")
    email: EmailStr = Field(..., description="Enter your email.")
    password: str = Field(..., min_length=8, description="Enter your password.")
    password_confirm: str = Field(..., min_length=8, description="Confirm your password.")


class UserLogin(UserBase):
    password: str


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    patronymic: str | None = None
    email: EmailStr
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)