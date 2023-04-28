from sqlalchemy.orm import Session

from database.models import App, Product, Transaction, User


def get_user(db: Session, username: str) -> User:
    return db.query(User).filter(User.name == username).first()


def get_or_create_user(session: Session, user: str) -> User:
    db_user = get_user(session, user)
    if db_user:
        return db_user

    db_user = User(name=user, balance=10.0, number_transactions=0)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_app(session: Session, name: str) -> App:
    return session.query(App).filter(App.name == name).first()


def get_produt(session: Session, name: str) -> Product:
    return session.query(Product).filter(Product.name == name).first()


def get_store(session: Session) -> App:
    return session.query(App).filter(App.name == "AptoideStore#1").first()


def create_transaction(
    session: Session,
    amount: float,
    sender_id: int,
    app_id: int,
    store_id: int,
    product_id: int,
) -> Transaction:
    db_transaction = Transaction(
        amount=amount,
        sender=sender_id,
        app_id=app_id,
        store_id=store_id,
        product_id=product_id,
    )
    session.add(db_transaction)
    session.commit()
    session.refresh(db_transaction)

    return db_transaction
