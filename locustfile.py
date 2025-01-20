from locust import HttpUser, task, constant
from app.schemas import OperationType


class WalletUser(HttpUser):
    wait_time = constant(0)
    host = "http://localhost:5000"

    @task(1)
    def get_wallet_balance(self):
        wallet_uuid = "d0c716e0-bdac-49d9-b0d8-fc1215e69027"
        self.client.get(f"/api/v1/wallets/{wallet_uuid}/balance")

    @task(2)
    def modify_wallet(self):
        wallet_uuid = "d0c716e0-bdac-49d9-b0d8-fc1215e69027"
        params = {"operationType": OperationType.DEPOSIT.value, "amount": 100.0}
        self.client.post(f"/api/v1/wallets/{wallet_uuid}/operation", params=params)
