from datetime import datetime
from pydantic import BaseModel
from schemas import user_schemas
from typing import List


class Plan(BaseModel):
    name: str
    amount: int
    active: bool
    canCashOut: bool
    softDelete: bool
    createdAt: datetime
    updatedAt: datetime

class UserPlan(user_schemas.UserBase):
    plans_data: List[Plan]