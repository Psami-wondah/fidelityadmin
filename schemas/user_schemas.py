from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    uin: str
    username: str
    wallet: str
    email: EmailStr
    isEmailVerified: bool
    refferals: list
    plans: list
    createdAt: datetime
    updatedAt: datetime


class User(UserBase):
    password: str
    profile_pic: Optional[str]
    document: Optional[str]
    address: Optional[str]
    btc_wallet: Optional[str]
    city: Optional[str]
    contact: Optional[str]
    country: Optional[str]
    name: Optional[str]
