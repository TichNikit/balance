import requests

from app.schemas import OperationType


def test_get_all_wallets():
    response = requests.get(
        'http://localhost:5000/api/v1/wallets/get_all')
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_get_balance_existing_wallet():
    wallet_uuid = "d0c716e0-bdac-49d9-b0d8-fc1215e69027"
    response = requests.get(f'http://localhost:5000/api/v1/wallets/{wallet_uuid}/balance')

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["wallet_uuid"] == wallet_uuid


def test_get_balance_non_existing_wallet():
    wallet_uuid = "non-existing-uuid"
    response = requests.get(
        f'http://localhost:5000/api/v1/wallets/{wallet_uuid}/balance')

    assert response.status_code == 404
    assert response.json() == {"detail": "Wallet not found"}


def test_modify_wallet():
    wallet_uuid = "d0c716e0-bdac-49d9-b0d8-fc1215e69027"

    response = requests.post(
        f'http://localhost:5000/api/v1/wallets/{wallet_uuid}/operation',
        params={"operationType": OperationType.DEPOSIT.value, "amount": 100.0}
    )

    response_data = response.json()
    assert response.status_code == 200
    assert response_data["wallet_uuid"] == wallet_uuid
    assert "new_balance" in response_data


def test_modify_wallet_non_existing_wallet():
    wallet_uuid = "non-existing-uuid"
    response = requests.post(
        f'http://localhost:5000/api/v1/wallets/{wallet_uuid}/operation',
        params={"operationType": OperationType.DEPOSIT.value, "amount": 100.0}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Wallet not found"}


def test_wallet_creator():
    new_wallet_data = {
        "balance": 0.0
    }
    response = requests.post('http://localhost:5000/api/v1/wallets/one', json=new_wallet_data)

    assert response.status_code == 200
    assert "message" in response.json()


if __name__ == '__main__':
    test_get_all_wallets()
    test_get_balance_existing_wallet()
    test_get_balance_non_existing_wallet()
    test_modify_wallet()
    test_modify_wallet_non_existing_wallet()
    test_wallet_creator()
