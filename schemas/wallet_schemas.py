from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Wallet(BaseModel):
    cash_balance: int
    profit: int
    refferalProfit: int
    depositBalance: int
    withdrawBalance: int
    createdAt: datetime
    updatedAt: datetime

class WalletUpdate(BaseModel):
    cash_balance: Optional[int]
    profit: Optional[int]
    refferalProfit: Optional[int]
    depositBalance: Optional[int]
    withdrawBalance: Optional[int]
