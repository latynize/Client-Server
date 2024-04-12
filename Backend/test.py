import pytest
from httpx import AsyncClient
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from main import app 
import ORM.tables as t 
import ORM.mapper as m  

TEST_DATABASE_URL = "postgresql+asyncpg://postgres:post@localhost/test_postgres"

@pytest.fixture
async def override_get_db():
    engine = create_async_engine(TEST_DATABASE_URL, future=True, echo=True)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
    
    async with engine.begin() as conn:
        await conn.run_sync(m.Base.metadata.create_all)
    
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        await db.close()
        async with engine.begin() as conn:
            await conn.run_sync(m.Base.metadata.drop_all)

@pytest.fixture
def test_app(override_get_db):
    app.dependency_overrides[m.get_db_session] = override_get_db
    yield app

@pytest.mark.anyio
async def test_get_employees(test_app):
    async with AsyncClient(app=test_app, base_url="http://testserver") as ac:
        response = await ac.get("/api/employee/")
        assert response.status_code == 200
        assert response.json() == {"employee": []}

@pytest.mark.anyio
async def test_delete_employee_not_found(test_app):
    async with AsyncClient(app=test_app, base_url="http://testserver") as ac:
        response = await ac.delete("/api/employee/999/")
        assert response.status_code == 404
        assert response.json() == {"detail": "Employee not found"}
