from typing import List, Optional

from pydantic import BaseModel


class UserData(BaseModel):
    user: str
    user_balance: float


class AppData(BaseModel):
    app: str
    app_balance: float


class TransactionValue(BaseModel):
    transaction_id: int
    amount: float
    product: str

    user_data: UserData
    app_data: List[AppData]

    # Type of transaction: buying product or savings
    type: str


class TransactionRequest(BaseModel):
    app: str
    product: str
    user: str

    class Config:
        orm_mode = True


class TransactionResponse(BaseModel):
    payment: Optional[TransactionValue] = None
    savings: Optional[TransactionValue] = None

    error: Optional[str] = None

    class Config:
        orm_mode = True
