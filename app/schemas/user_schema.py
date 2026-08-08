from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class UserUpdateRequest(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None

class UsernameCheckResponse(BaseModel):
    username: str
    is_available: bool
