from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import datetime
from uuid import UUID

class UsersPOSTSchemas(BaseModel):
    username: str
    email: EmailStr
    password: bytes
    model_config = ConfigDict(from_attributes=True)

class UsersGETSchemas(UsersPOSTSchemas):
    id: UUID
    password: bytes = Field(..., exclude=True)
    active: bool
    created_at: datetime
    updated_at: datetime

class UsersPUTSchemas(UsersPOSTSchemas):
    id: UUID