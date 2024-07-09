import pytest
from fastapi.testclient import TestClient
from main import app
from ORM.mapper import Mapper
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient
import os
from dotenv import load_dotenv

@pytest.fixture(scope="module")
async def async_client():
    load_dotenv()
    test_url = os.getenv("TEST_DB")
    async with AsyncClient(app=app, base_url=test_url) as ac:
        yield ac

@pytest.fixture(scope="module")
async def setup_db():
    mapper = Mapper()
    await mapper.reflect_tables()
    async with mapper.get_db_session() as db:
        yield db
