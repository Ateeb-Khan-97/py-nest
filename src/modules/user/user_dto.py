from datetime import datetime
from pydantic import BaseModel, Field


class UsersResponseDto(BaseModel):
    id: int = Field(..., description="ID")
    fullname: str = Field(..., description="Full Name")
    email: str = Field(..., description="Email")
    created_at: datetime = Field(..., description="Created At")
    updated_at: datetime = Field(..., description="Updated At")


class UsersUpdateDto(BaseModel):
    fullname: str = Field(..., min_length=3, description="Full Name")
