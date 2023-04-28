from typing import List

from sqlmodel import Session

from app.services import calculate_discount
from app.values import AppData, TransactionValue, UserData
from database.queries import (create_transaction, get_app, get_or_create_user,
                              get_produt, get_store)


class TransactionException(Exception):
    pass


def make_transactions(
    session: Session, app: str, product: str, user: str
) -> List[TransactionValue]:
    """
    Function in charge to creating the transactions, updating the DB
    and responding with the values required by the API.

    The main logic is wrapped in a try/expect so that if the transaction
    fails for any reason we do not update any objects.
    """
    db_user = get_or_create_user(session, user)
    db_app = get_app(session, app)
    db_product = get_produt(session, product)
    db_store = get_store(session)
    product_amount = db_product.amount

    if db_user.balance - product_amount < 0:
        raise ValueError("Not enough balance")

    # App updates
    db_app.balance += product_amount * 75 / 100

    # Store updates
    db_store.balance += product_amount * 25 / 100

    transactions = []
    try:
        db_transaction = create_transaction(
            session=session,
            amount=product_amount,
            sender_id=db_user.id,
            app_id=db_app.id,
            store_id=db_store.id,
            product_id=db_product.id,
        )

        db_user.balance -= db_product.amount

        transactions.append(
            TransactionValue(
                transaction_id=db_transaction.id,
                amount=product_amount,
                product=product,
                user_data=UserData(user=user, user_balance=db_user.balance),
                app_data=[
                    AppData(app=db_app.id, app_balance=db_app.balance),
                    AppData(app=db_store.id, app_balance=db_store.balance),
                ],
                type="payment",
            )
        )

        # Check if we need to apply a discount to this transaction
        discount = calculate_discount(db_user.number_transactions)

        if discount:
            savings = db_product.amount * discount / 100

            db_transaction_discount = create_transaction(
                session=session,
                amount=savings,
                sender_id=db_user.id,
                app_id=db_app.id,
                store_id=db_store.id,
                product_id=db_product.id,
            )

            # User updates
            db_user.balance += savings
            db_store.balance -= savings
    except Exception as e:
        raise TransactionException("Transaction not processed corretly!" + e)

    # User updates
    db_user.number_transactions += 1

    session.commit()
    session.refresh(db_user)
    session.refresh(db_app)
    session.refresh(db_store)

    if discount:
        transactions.append(
            TransactionValue(
                transaction_id=db_transaction_discount.id,
                amount=savings,
                product=product,
                user_data=UserData(user=user, user_balance=db_user.balance),
                app_data=[
                    AppData(app=db_store.id, app_balance=db_store.balance)
                ],
                type="savings",
            )
        )

    return transactions
