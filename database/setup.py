from sqlmodel import Session

from database.models import App, Product


def setup_db(session: Session):
    create_app(session=session, id="AptoideStore", name="AptoideStore#1")

    trivia_developer_app = create_app(
        session=session,
        id="TrivialDriveDeveloper#2",
        name="TrivialDrive",
    )

    diamond_league_app = create_app(
        session=session,
        id="DiamondLegendDeveloper#3",
        name="DiamondLegend",
    )

    create_product(
        session=session,
        name="Oil",
        amount=1.0,
        app_id=trivia_developer_app.id,
        app=trivia_developer_app,
    )

    create_product(
        session=session,
        name="Antifreeze",
        amount=1.2,
        app_id=trivia_developer_app.id,
        app=trivia_developer_app,
    )

    create_product(
        session=session,
        name="5x_Diamonds",
        amount=2.0,
        app_id=diamond_league_app.id,
        app=diamond_league_app,
    )


def create_app(
    session: Session, id: str, name: str, balance: float = 10.0
) -> App:
    app = App(id=id, name=name, balance=balance)
    session.add(app)
    session.commit()
    session.refresh(app)

    return app


def create_product(
    session: Session, name: str, amount: float, app_id: str, app: App
) -> None:
    product = Product(
        name=name,
        amount=amount,
        app_id=app_id,
        app=app,
    )
    session.add(product)
    session.commit()
    session.refresh(product)
