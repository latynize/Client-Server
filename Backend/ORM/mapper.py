from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import MetaData, text
from dotenv import load_dotenv
import os

class Mapper:
    def __init__(self):
        """
        Initializes the PostgreSQL engine, session, metadata, and automatic mapping.
        """
        load_dotenv()
        postgresql_url = os.getenv("POSTGRESQL_DB")
        if not postgresql_url:
            raise ValueError("POSTGRESQL_DB environment variable not set.")
        
        self.engine = create_async_engine(
            postgresql_url
        )
        self.SessionLocal = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )
        self.metadata = MetaData()
        self.Base = automap_base()

    async def reflect_tables(self, schema="cioban") -> None:
        """
        Reflects the tables of the given schema and prepares the ORM.
        
        :param schema: The schema to reflect.
        """
        async with self.engine.begin() as conn:
            await conn.run_sync(self.metadata.reflect, schema=schema)
            await conn.run_sync(self.Base.prepare, reflect=True, schema=schema)

    async def get_db_session(self):
        """
        Generates a session to the database schema "cioban".
        
        :return: An asynchronous generator yielding the database session.
        """
        async with self.SessionLocal() as session:
            try:
                await session.execute(text("SET search_path TO cioban"))
                yield session
            except Exception as e:
                print(f"Error during session execution: {e}")
                raise
            finally:
                await session.close()

    async def get_db_session_login(self):
        """
        Generates a session to the database schema "login".
        
        :return: An asynchronous generator yielding the database session.
        """
        async with self.SessionLocal() as session:
            try:
                await session.execute(text("SET search_path TO login"))
                yield session
            except Exception as e:
                print(f"Error during session execution: {e}")
                raise
            finally:
                await session.close()
