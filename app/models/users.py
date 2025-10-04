from uuid import UUID
from typing import Optional
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: UUID
    username: str
    email: str


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class LoginRequest(BaseModel):
    username: Optional[str]
    email: Optional[str]
    password: str
