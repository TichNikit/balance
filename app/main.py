from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.db import create_table
from app.routers.router_1 import router_wallets


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_table()
    print("База готова")
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(router_wallets)
