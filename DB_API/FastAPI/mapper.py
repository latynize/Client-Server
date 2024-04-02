from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import text
from sqlalchemy.future import select


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

    def model_to_dict(self, model_instance, exclude_columns=None, order_columns=None):
        exclude_columns = set(exclude_columns or [])
        order_columns = order_columns or []
        
        result_dict = {}
        
        if hasattr(model_instance.__class__, '__table__'):
            table = model_instance.__class__.__table__
            
            for column_name in order_columns:
                if column_name in table.c and column_name not in exclude_columns:
                    result_dict[column_name] = getattr(model_instance, column_name)
            
            for column in table.c:
                if column.name not in exclude_columns and column.name not in result_dict:
                    result_dict[column.name] = getattr(model_instance, column.name)
        else:
            raise AttributeError("Model instance does not have a '__table__' attribute.")
        
        return result_dict

async def universal_delete(self, session, model_instance, **conditions) -> None:

    query = select(model_instance)
    for attr, value in conditions.items():
        query = query.filter(getattr(model_instance, attr) == value)

    results = await session.execute(query)
    instances = results.scalars().all()

    if not instances:
        return False 

    for instance in instances:
        await session.delete(instance)

    await session.commit()
    return True  
