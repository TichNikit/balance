from pydantic import BaseModel
import enum


class OperationType(str, enum.Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


class Operation(BaseModel):
    operationType: OperationType
    amount: float


class CreateWallet(BaseModel):
    balance: float = 0
