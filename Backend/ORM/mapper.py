from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import MetaData, text


class Mapper:

    # Initialisiert PostgreSQL-Verbindung, Session, Metadaten und automatisches Mapping
    def __init__(self):
        self.engine = create_async_engine("postgresql+asyncpg://postgres:post@localhost/postgres", echo=True)
        self.SessionLocal = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)
        self.metadata = MetaData()
        self.Base = automap_base()

    # Reflektiert die Tabellen der Datenbank als Metadaten
    async def reflect_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(self.metadata.reflect, schema="cioban")
            await conn.run_sync(self.Base.prepare, reflect=True, schema="cioban")

    # Generiert eine Session zur Datenbank und dem Schema "cioban"
    async def get_db_session(self) -> AsyncSession:
        async with self.SessionLocal() as session:
            await session.execute(text("SET search_path TO cioban"))
            yield session

