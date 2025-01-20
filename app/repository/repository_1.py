from fastapi import HTTPException
from sqlalchemy import select, insert, update
from sqlalchemy.exc import NoResultFound
from app.db.db import Wallets, SessionLocal
from app.schemas import CreateWallet, Operation


class WalletsRepository:
    @classmethod
    async def get_all_wallets(cls):
        async with SessionLocal() as session:
            task = select(Wallets)
            result = await session.execute(task)
            wallets = result.scalars().all()
            return wallets

    @classmethod
    async def creat_one_wallet(cls, wallet: CreateWallet):
        async with SessionLocal() as session:
            task = insert(Wallets).values(
                balance=wallet.balance
            )
            result = await session.execute(task)
            country_id = result.inserted_primary_key[0]
            await session.commit()
        return country_id

    @classmethod
    async def modify_wallet(cls, wallet_uuid: str, operation: Operation):
        async with SessionLocal() as session:
            async with session.begin():
                task = select(Wallets).where(Wallets.id == wallet_uuid).with_for_update()
                result = await session.execute(task)

                try:
                    wallet = result.scalar_one()
                except NoResultFound:
                    return None

                if operation.operationType == "DEPOSIT":
                    new_balance = wallet.balance + operation.amount
                elif operation.operationType == "WITHDRAW":
                    if wallet.balance < operation.amount:
                        raise HTTPException(status_code=400, detail="Insufficient funds")
                    new_balance = wallet.balance - operation.amount
                else:
                    raise HTTPException(status_code=400, detail="Unknown operation type")

                await session.execute(
                    update(Wallets).where(Wallets.id == wallet_uuid).values(balance=new_balance)
                )

            await session.commit()
        return {"wallet_uuid": wallet_uuid, "new_balance": new_balance}

    @classmethod
    async def get_balance(cls, wallet_uuid: str):
        async with SessionLocal() as session:
            task = select(Wallets).where(Wallets.id == wallet_uuid)
            result = await session.execute(task)
            try:
                wallet = result.scalar_one()
                return wallet.balance
            except NoResultFound:
                raise HTTPException(status_code=404, detail="Wallet not found")
