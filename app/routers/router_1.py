from fastapi import APIRouter, Depends, HTTPException
from app.repository.repository_1 import WalletsRepository
from typing import Annotated
from app.schemas import CreateWallet, Operation

router_wallets = APIRouter(prefix='/api/v1/wallets', tags=['Кошельки'])


@router_wallets.get('/get_all')
async def all_wallets():
    wallets = await WalletsRepository.get_all_wallets()

    return {'wallets': wallets}


@router_wallets.get('/{wallet_uuid}/balance')
async def get_balance(wallet_uuid: str):
    balance = await WalletsRepository.get_balance(wallet_uuid)

    if balance is None:
        raise HTTPException(status_code=404, detail="Wallet not found")

    return {"wallet_uuid": wallet_uuid, "balance": balance}


@router_wallets.post('/{wallet_uuid}/operation')
async def modify_wallet(wallet_uuid: str, operation: Annotated[Operation, Depends()]):
    result = await WalletsRepository.modify_wallet(wallet_uuid, operation)

    if result is None:
        raise HTTPException(status_code=404, detail="Wallet not found")

    return result


@router_wallets.post('/one')
async def wallet_creator(wallet: Annotated[CreateWallet, Depends()]):
    wallets = await WalletsRepository.creat_one_wallet(wallet)
    return {'message': f'Создан новый кошелёк: {wallets}'}
