from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import text



class Mapper:
    def __init__(self):
        self.engine = create_async_engine("postgresql+asyncpg://postgres:post@localhost/postgres", echo=True)
        self.SessionLocal = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)
        self.Base = automap_base()

    async def reflect_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(self.Base.prepare, reflect=True, schema="cioban")

    async def get_db_session(self) -> AsyncSession:
        async with self.SessionLocal() as session:
            await session.execute(text("SET search_path TO cioban"))
            yield session

    def model_to_list(self, model_instance, exclude_columns=None, order_columns=None, additional_fields=None):
        exclude_columns = set(exclude_columns or [])
        order_columns = order_columns or []
        additional_fields = additional_fields or {}

        model_list = {}
        for column_name in order_columns:
            if column_name in model_instance.__class__.__table__.c and column_name not in exclude_columns:
                model_list[column_name] = getattr(model_instance, column_name)

        for key, value in additional_fields.items():
            if key in order_columns:
                model_list[key] = value

        ordered_list = {}
        for column_name in order_columns:
            if column_name in model_list:
                ordered_list[column_name] = model_list[column_name]

        return ordered_list
