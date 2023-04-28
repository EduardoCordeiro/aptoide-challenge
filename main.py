import os

from fastapi import Depends, FastAPI, Response
from sqlmodel import Session, SQLModel, create_engine

from app.transactions import TransactionException, make_transactions
from app.values import TransactionRequest, TransactionResponse
from database.setup import setup_db

SQL_DATABASE_URL = "sqlite:///./sql_app.db"

app = FastAPI()

engine = create_engine(SQL_DATABASE_URL, echo=False)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


@app.on_event("startup")
def startup():
    create_db_and_tables()
    setup_db(Session(engine))


@app.on_event("shutdown")
def shutdow():
    os.remove("sql_app.db")


@app.get("/health")
def health():
    return "Healthy"


@app.post("/transaction")
def transaction(
    transaction: TransactionRequest,
    response: Response,
    session: Session = Depends(get_session),
):
    try:
        transactions = make_transactions(
            session=session,
            app=transaction.app,
            product=transaction.product,
            user=transaction.user,
        )

        response = TransactionResponse()
        for t in transactions:
            if t.type == "payment":
                response.payment = t
            elif t.type == "savings":
                response.savings = t

        return response
    except ValueError as ve:
        response.status_code = 500
        return TransactionResponse(error=str(ve))
    except TransactionException as te:
        return TransactionResponse(error=str(te))
