from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from schemas import admin_schemas


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None

class AdminToken(Token):
    admin: admin_schemas.AdminGet
    expires: datetime
