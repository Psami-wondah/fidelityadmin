from datetime import datetime
from pydantic import BaseModel
from db.config import db
from typing import Any


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


class AdminCreate(AdminBase):
    password: str
