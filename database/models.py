from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    name: str
    balance: float
    number_transactions: int


class App(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)

    name: str
    balance: float

    items: Optional[List["Product"]] = Relationship(back_populates="app")


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    name: str
    amount: float

    app_id: int = Field(default=None, foreign_key="app.id")
    app: Optional[App] = Relationship(back_populates="items")


class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    amount: float

    sender: int = Field(default=None, foreign_key="user.id")
    app_id: int = Field(default=None, foreign_key="app.id")
    store_id: int = Field(default=None, foreign_key="app.id")
    product_id: int = Field(default=None, foreign_key="product.id")
