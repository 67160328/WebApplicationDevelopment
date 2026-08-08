from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserRegisterRequest(BaseModel):
    username: str = Field(..., example="johndoe", min_length=3)
    email: str = Field(..., example="john@example.com")
    password: str = Field(..., example="securepassword123", min_length=6)
    full_name: Optional[str] = Field(None, example="John Doe")

class UserLoginRequest(BaseModel):
    username: str = Field(..., example="johndoe")
    password: str = Field(..., example="securepassword123")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=6)
