from datetime import datetime
from pydantic import BaseModel
from db.config import db
from typing import Any, Optional


class AdminBase(BaseModel):
    username: str
    first_name: str
    last_name: str

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self.username = self.username.lower()

    @staticmethod
    def init():
        db.admins.create_index([("username", 1)], unique=True)


class Admin(AdminBase):
    hashed_password: str
    is_superuser: bool
    created_at: datetime
    last_updated_at: datetime
    profile_image_url: Optional[str]


class AdminCreate(AdminBase):
    password: str


class AdminUpdate(BaseModel):
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    profile_image_url: Optional[str]
    last_updated_at: datetime
