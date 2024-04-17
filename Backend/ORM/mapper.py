from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import MetaData, text


# This module provides the Mapper class, which is responsible for the ORM setup. It uses the SQLAlchemy library to
# reflect the tables of the database schemas and to generate sessions to these schemas.


class Mapper:

    def __init__(self):
        """
        Initializes the PostgreSQL engine, session, metadata, and automatic mapping.
        """
        self.engine = create_async_engine("postgresql+asyncpg://postgres:post@localhost/postgres")
        self.SessionLocal = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)
        self.metadata = MetaData()
        self.Base = automap_base()

    async def reflect_tables(self, schema: str = "cioban") -> None:
        """
        Reflects the tables of the given schema and prepares the ORM.
        :param String schema: The schema to reflect.
        """
        async with self.engine.begin() as conn:
            await conn.run_sync(self.metadata.reflect, schema=schema)
            await conn.run_sync(self.Base.prepare, reflect=True, schema=schema)

    async def get_db_session(self) -> AsyncSession:
        """
        Generates a session to the database schema "cioban".
        :return: AsyncSession session: The database session.
        """
        async with self.SessionLocal() as session:
            await session.execute(text("SET search_path TO cioban"))
            yield session

    async def get_db_session_login(self) -> AsyncSession:
        """
        Generates a session to the database schema "login".
        :return: AsyncSession session: The database session.
        """
        async with self.SessionLocal() as session:
            await session.execute(text("SET search_path TO login"))
            yield session
