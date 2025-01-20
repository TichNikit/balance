import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import uuid

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# подключение через Докер
database_url = os.getenv('DATABASE_URL')
engine = create_async_engine(database_url)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


# подключение на прямую
# engine = create_async_engine("postgresql+asyncpg://postgres:nikitatnm2@localhost/balance")
# SessionLocal = async_sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass


class Wallets(Base):
    __tablename__ = "wallets"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    balance: Mapped[float] = mapped_column(default=0)


async def create_table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
