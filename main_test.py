from fastapi.testclient import TestClient


def test_transaction_api(client: TestClient):
    response = client.post(
        "/transaction/",
        json={"app": "TrivialDrive", "product": "Oil", "user": "User#123"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "payment": {
            "transaction_id": 1,
            "amount": 1.0,
            "product": "Oil",
            "user_data": {"user": "User#123", "user_balance": 9.0},
            "app_data": [
                {
                    "app": "TrivialDriveDeveloper#2",
                    "app_balance": 10.75,
                },
                {
                    "app": "AptoideStore",
                    "app_balance": 10.25,
                },
            ],
            "type": "payment",
        },
        "savings": None,
        "error": None,
    }
