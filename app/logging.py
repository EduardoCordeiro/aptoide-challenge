from typing import Dict


def log_payment(
    transaction_id: int,
    app: str,
    product: str,
    amount: float,
    sender: str,
    receivers: Dict[str, str],
):
    print(
        f"PURCHASE TRANSACTION => id: {transaction_id}; app: {app}; item: {product}; amount: €{round(amount, 2)}; sender: {sender}; receivers: {receivers}"  # noqa
    )


def log_balance(
    user: str,
    user_balance: float,
    receivers: Dict[str, float],
) -> None:
    print(f"BALANCE => {user}: €{round(user_balance, 2)}; {receivers}")  # noqa


def log_reward(
    transaction_id: int,
    amount: float,
    sender: str,
    receivers: Dict[str, float],
):
    print(
        f"REWARD TRANSACTION => id: {transaction_id}; amount: €{round(amount, 2)}; sender: {sender}; receivers: {receivers}"  # noqa
    )
