from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


# class PostBase(BaseModel):
#     title: str
#     content: str
#     published: bool = True


# class PostCreate(PostBase):
#     pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    surname: str
    profile_image: str
    created_at: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserVerifyEmail(BaseModel):
    email: EmailStr


class ResetPassword(BaseModel):
    email: EmailStr
    password: str
    verification_code: int


class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int


class TokenData(BaseModel):
    id: Optional[str] = None
