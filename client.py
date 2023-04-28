import json
import sys

import requests

from app.logging import log_balance, log_payment, log_reward
from app.values import TransactionValue

data = {"app": sys.argv[1], "product": sys.argv[2], "user": sys.argv[3]}

r = requests.post(
    url="http://localhost:8000/transaction",
    headers={"Content-Type": "application/json"},
    data=json.dumps(data),
)

json_data = r.json()

error = json_data.get("error")
payment_data = json_data.get("payment", None)
savings_data = json_data.get("savings", None)


if error:
    print(error)
    exit(1)

payment = TransactionValue.parse_obj(payment_data)
if savings_data:
    savings = TransactionValue.parse_obj(savings_data)

log_payment(
    transaction_id=payment.transaction_id,
    app=payment.app_data[0].app,
    product=payment.product,
    amount=payment.amount,
    sender=payment.user_data.user,
    receivers={app.app: app.app_balance for app in payment.app_data},
)

log_balance(
    user=payment.user_data.user,
    user_balance=payment.user_data.user_balance,
    receivers={app.app: app.app_balance for app in payment.app_data},
)


if savings_data:
    print("#########")
    log_reward(
        transaction_id=savings.transaction_id,
        amount=savings.amount,
        sender=savings.app_data[0].app,
        receivers={savings.user_data.user: savings.amount},
    )
    log_balance(
        user=savings.user_data.user,
        user_balance=savings.user_data.user_balance,
        receivers={app.app: app.app_balance for app in savings.app_data},
    )
