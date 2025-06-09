import asyncio
from core.models.base import Base
from core.models.db_helper import db_helper_mock

async def create_all_mock_tables():
    async with db_helper_mock.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Тестовые базы данных созданы")


if __name__=="__main__":
    asyncio.run(create_all_mock_tables())