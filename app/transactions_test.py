from app.transactions import make_transactions
from app.values import AppData, TransactionValue, UserData


def test_make_transactions(session):
    app = "DiamondLegend"
    product = "5x_Diamonds"
    user = "TestUser#1"

    expected = [
        TransactionValue(
            transaction_id=1,
            amount=2.0,
            product="5x_Diamonds",
            user_data=UserData(user="TestUser#1", user_balance=8.0),
            app_data=[
                AppData(app="DiamondLegendDeveloper#3", app_balance=11.5),
                AppData(app="AptoideStore", app_balance=10.5),
            ],
            type="payment",
        )
    ]

    assert make_transactions(session, app, product, user) == expected
