from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import text


class Mapper:
    def __init__(self):
        self.engine = create_async_engine("postgresql+asyncpg://postgres:post@localhost/postgres", echo=True)
        self.SessionLocal = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False) #Warum nicht async_sessionmaker?
        self.Base = automap_base()

    async def reflect_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(self.Base.prepare, reflect=True, schema="cioban")

    async def get_db_session(self) -> AsyncSession:
        async with self.SessionLocal() as session:
            await session.execute(text("SET search_path TO cioban"))
            yield session

    def model_to_dict(self, model_instance, exclude_columns=None):
        exclude_columns = exclude_columns or []
        if hasattr(model_instance.__class__, '__table__'):
            table = model_instance.__class__.__table__
        return {
            column.name: getattr(model_instance, column.name)
            for column in table.columns
            if column.name not in exclude_columns
        }
