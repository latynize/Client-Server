import pytest
from httpx import AsyncClient
from .main import app
from ORM.mapper import Mapper
from helper import Helper as h
import ORM.tables as t
import main

m = Mapper()
app = main.app

class test:

    # Assuming you have a function in your app to create all tables
    async def test_tables():
        async with m.reflect_tables() as conn:
            await conn.run_sync(m.Base.metadata.create_all)

    # Setup Test Database URL
    TEST_DATABASE_URL = "postgresql+asyncpg://postgres:post@localhost/postgres"
    engine = create_async_engine(TEST_DATABASE_URL, future=True, echo=True)

    # Session fixture for dependency override
    @pytest.fixture
    async def override_get_db(engine):
        async_session = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )
        async with async_session() as session:
            yield session

    @pytest.fixture
    async def test_app():
        # Create test tables
        await test_tables()

        # Dependency override
        app.dependency_overrides[app.get_db_session] = override_get_db()

        async with AsyncClient(app=app, base_url="http://test") as ac:
            yield ac  # use httpx AsyncClient for async requests

        # Optionally, drop test tables after tests are done
async def test_root():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Tomato"}