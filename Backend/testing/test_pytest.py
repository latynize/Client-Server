import pytest
from httpx import AsyncClient
from app.main import app
from app.ORM.tables import Employee, Project, Team, ConnectionTeamEmployee, Department, Type, ExperienceLevel, Skill, Address, EducationDegree, Job, Internal, External, Stat
from app.ORM.mapper import Mapper
from app.helper import Helper
from dotenv import load_dotenv
import os

load_dotenv()

test_url = os.getenv("TEST_DB")

# Set up fixtures for test data
@pytest.fixture(scope="module")
async def async_client():
    async with AsyncClient(app=app, base_url=test_url) as ac:
        yield ac

@pytest.fixture(scope="module")
async def setup_db():
    # Add any setup code to create test data here
    mapper = Mapper()
    await mapper.reflect_tables()
    async with mapper.get_db_session() as db:
        # Example: add test employee
        new_employee = Employee(
            first_name="Test",
            last_name="User",
            base_fte=1.0,
            free_fte=1.0,
            e_mail="test.user@example.com",
            phone_number="1234567890",
            entry_date="2024-01-01",
            experience_level_id=1,
            type_id=1,
            address_id=1
        )
        db.add(new_employee)
        await db.commit()

@pytest.mark.asyncio
async def test_create_employee(async_client, setup_db):
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "base_fte": 1.0,
        "free_fte": 1.0,
        "e_mail": "john.doe@example.com",
        "phone_number": "9876543210",
        "entry_date": "2024-01-01",
        "experience_level_id": 1,
        "type_id": 1,
        "address_id": 1
    }
    response = await async_client.post("/api/employee/", json=data)
    assert response.status_code == 200
    assert response.json()["message"] == "Employees created successfully"

@pytest.mark.asyncio
async def test_get_employee(async_client):
    response = await async_client.get("/api/employee/")
    assert response.status_code == 200
    assert "employee" in response.json()

@pytest.mark.asyncio
async def test_get_employee_by_id(async_client, setup_db):
    response = await async_client.get("/api/employee/1/")
    assert response.status_code == 200
    assert "employee" in response.json()

@pytest.mark.asyncio
async def test_update_employee(async_client, setup_db):
    data = {
        "first_name": "Jane",
        "last_name": "Doe",
        "base_fte": 0.8,
        "free_fte": 0.8,
        "e_mail": "jane.doe@example.com",
        "phone_number": "1231231230",
        "entry_date": "2024-02-01",
        "experience_level_id": 2,
        "type_id": 2,
        "address_id": 2
    }
    response = await async_client.put("/api/employee/1/", json=data)
    assert response.status_code == 200
    assert response.json()["message"] == "Employee updated successfully."

@pytest.mark.asyncio
async def test_delete_employee(async_client, setup_db):
    response = await async_client.delete("/api/employee/1/")
    assert response.status_code == 200
    assert response.json()["message"] == "Employee deleted successfully."

@pytest.mark.asyncio
async def test_create_project(async_client, setup_db):
    data = {
        "department_id": 1,
        "proj_name": "New Project",
        "proj_priority": "High",
        "proj_manager": 1,
        "needed_fte": 5.0,
        "current_fte": 2.0,
        "start_date": "2024-01-01",
        "end_date": "2024-12-31"
    }
    response = await async_client.post("/api/project/", json=data)
    assert response.status_code == 200
    assert response.json()["message"] == "Project created successfully"

@pytest.mark.asyncio
async def test_get_project(async_client):
    response = await async_client.get("/api/project/")
    assert response.status_code == 200
    assert "project" in response.json()

@pytest.mark.asyncio
async def test_get_project_by_id(async_client, setup_db):
    response = await async_client.get("/api/project/1/")
    assert response.status_code == 200
    assert "project" in response.json()

@pytest.mark.asyncio
async def test_update_project(async_client, setup_db):
    data = {
        "department_id": 1,
        "proj_name": "Updated Project",
        "proj_priority": "Low",
        "proj_manager": 1,
        "needed_fte": 3.0,
        "current_fte": 1.0,
        "start_date": "2024-02-01",
        "end_date": "2024-11-30"
    }
    response = await async_client.put("/api/project/1/", json=data)
    assert response.status_code == 200
    assert response.json()["message"] == "Project updated successfully."

@pytest.mark.asyncio
async def test_delete_project(async_client, setup_db):
    response = await async_client.delete("/api/project/1/")
    assert response.status_code == 200
    assert response.json()["message"] == "Project deleted successfully."

@pytest.mark.asyncio
async def test_get_internal(async_client):
    response = await async_client.get("/api/internal/")
    assert response.status_code == 200
    assert "internal" in response.json()

@pytest.mark.asyncio
async def test_get_external(async_client):
    response = await async_client.get("/api/external/")
    assert response.status_code == 200
    assert "external" in response.json()

@pytest.mark.asyncio
async def test_get_stat(async_client):
    response = await async_client.get("/api/stat/")
    assert response.status_code == 200
    assert "stat" in response.json()

@pytest.mark.asyncio
async def test_get_department(async_client):
    response = await async_client.get("/api/department/")
    assert response.status_code == 200
    assert "department" in response.json()

@pytest.mark.asyncio
async def test_get_address(async_client):
    response = await async_client.get("/api/address/")
    assert response.status_code == 200
    assert "address" in response.json()

@pytest.mark.asyncio
async def test_get_type(async_client):
    response = await async_client.get("/api/type/")
    assert response.status_code == 200
    assert "type" in response.json()

@pytest.mark.asyncio
async def test_get_education_degree(async_client):
    response = await async_client.get("/api/education_degree/")
    assert response.status_code == 200
    assert "education_degree" in response.json()

@pytest.mark.asyncio
async def test_get_job(async_client):
    response = await async_client.get("/api/job/")
    assert response.status_code == 200
    assert "job" in response.json()

@pytest.mark.asyncio
async def test_get_skill(async_client):
    response = await async_client.get("/api/skill/")
    assert response.status_code == 200
    assert "skill" in response.json()

@pytest.mark.asyncio
async def test_get_experience_level(async_client):
    response = await async_client.get("/api/experience_level/")
    assert response.status_code == 200
    assert "experience_level" in response.json()

@pytest.mark.asyncio
async def test_login(async_client):
    data = {
        "username": "testuser",
        "password": "testpassword"
    }
    response = await async_client.post("/api/login/", json=data)
    assert response.status_code == 200
    assert response.json()["status"] == "success"

@pytest.mark.asyncio
async def test_verify_token(async_client):
    token_data = {
        "access_token": "your_jwt_token_here"
    }
    response = await async_client.post("/api/verifyToken", json=token_data)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
