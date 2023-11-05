from typing import Optional
from pydantic import BaseModel, EmailStr, PositiveInt


class User(BaseModel):
    id: int
    name: str


class UserAdult(BaseModel):
    name: str
    age: int


class Feedback(BaseModel):
    name: str
    message: str


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: Optional[PositiveInt] = None
    is_subscribed: Optional[bool] = None
