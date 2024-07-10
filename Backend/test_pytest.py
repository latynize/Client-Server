import pytest
from httpx import AsyncClient
from fastapi import status
import ORM.tables as t

BASE_URL = "http://127.0.0.1:8000"


@pytest.mark.anyio(asynclib_name="asyncio")
async def test_get_employee():
    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.get("/api/employee/")
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert "employee" in response_data


@pytest.mark.anyio(asynclib_name="asyncio")
async def test_get_employee_by_id():
    employee_id = 1
    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.get(f"/api/employee/{employee_id}/")
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert "employee" in response_data


@pytest.mark.anyio(asynclib_name="asyncio")
async def test_create_employee():
    new_employee = t.Employee(
        first_name="Andreas",
        last_name="Schmietendorf",
        base_fte=1.0,
        free_fte=1.0,
        e_mail="andreas.schmietendorf@test.de",
        phone_number="1234567890",
        entry_date="2024-01-01",
        experience_level_id=1,
        type_id=1,
        address_id=1,
    )
    employee_dict = new_employee.model_dump()
    employee_dict["entry_date"] = str(new_employee.entry_date)
    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.post("/api/employee/", json=employee_dict)
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["message"] == "Employees created successfully"


@pytest.mark.anyio(asynclib_name="asyncio")
async def test_update_employee():
    employee_id = 1
    update_data = t.Employee(
        first_name="Jane",
        last_name="Doe",
        base_fte=1.0,
        free_fte=0,
        e_mail="jane.doe@example.com",
        phone_number="0987654321",
        entry_date="2024-01-01",
        experience_level_id=1,
        type_id=1,
        address_id=1,
    )
    update_dict = update_data.model_dump()
    update_dict["entry_date"] = str(update_data.entry_date)
    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.put(f"/api/employee/{employee_id}/", json=update_dict)
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["message"] == "Employee updated successfully."


@pytest.mark.anyio(asynclib_name="asyncio")
async def test_delete_employee():
    employee_id = 2
    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.delete(f"/api/employee/{employee_id}/")
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["message"] == "Employee deleted successfully."


@pytest.mark.anyio(asynclib_name="asyncio")
async def test_search_employee():
    search_criteria = [
        {
            "department": "IT",
            "job": "Developer",
            "experienceLevel": "Senior",
            "project": "ProjectX",
            "type": "Full-Time",
            "skill": "Python",
            "fte": 1.0,
        }
    ]
    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.post("/api/search/", json=search_criteria)
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert "employee" in response_data


@pytest.mark.anyio(asynclib_name="asyncio")
async def test_get_project():
    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.get("/api/project/")
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert "project" in response_data


@pytest.mark.anyio(asynclib_name="asyncio")
async def test_get_project_by_id():
    project_id = 1
    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.get(f"/api/project/{project_id}/")
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert "project" in response_data


@pytest.mark.anyio(asynclib_name="asyncio")
async def test_create_project():
    new_project = t.Project(
        proj_name="New Project",
        department_id=1,
        proj_manager=1,
        proj_priority="High",
        needed_fte=5.0,
        current_fte=0.0,
        start_date="2024-01-01",
        end_date="2024-12-31",
    )
    project_dict = new_project.model_dump()
    project_dict["start_date"] = str(new_project.start_date)
    project_dict["end_date"] = str(new_project.end_date)
    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.post("/api/project/", json=project_dict)
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["message"] == "Project created successfully"


@pytest.mark.anyio(asynclib_name="asyncio")
async def test_update_project():
    project_id = 1
    update_data = t.Project(
        proj_name="Updated Project",
        department_id=1,
        proj_manager=1,
        proj_priority="Medium",
        needed_fte=5.0,
        current_fte=0.0,
        start_date="2024-01-01",
        end_date="2024-12-31",
    )
    update_dict = update_data.model_dump()
    update_dict["start_date"] = str(update_data.start_date)
    update_dict["end_date"] = str(update_data.end_date)
    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.put(f"/api/project/{project_id}/", json=update_dict)
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["message"] == "Project updated successfully."


@pytest.mark.anyio(asynclib_name="asyncio")
async def test_delete_project():
    project_id = 2
    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.delete(f"/api/project/{project_id}/")
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["message"] == "Project deleted successfully."


@pytest.mark.anyio(asynclib_name="asyncio")
async def test_get_team():
    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.get("/api/team/")
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert "team" in response_data


@pytest.mark.anyio(asynclib_name="asyncio")
async def test_get_team_by_id():
    team_id = 1
    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.get(f"/api/team/{team_id}/")
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert "team" in response_data


@pytest.mark.anyio(asynclib_name="asyncio")
async def test_create_team():
    new_team = t.Team(
        team_name="New Team",
        team_purpose="Development",
        project_id=1,
    )
    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.post("/api/team/", json=new_team.model_dump())
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["message"] == "Team created successfully"


@pytest.mark.anyio(asynclib_name="asyncio")
async def test_update_team():
    team_id = 2
    update_data = t.Team(
        team_name="Updated Team",
        team_purpose="Development",
        project_id=1,
    )
    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.put(f"/api/team/{team_id}/", json=update_data.model_dump())
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["message"] == "Team updated successfully."


@pytest.mark.anyio(asynclib_name="asyncio")
async def test_delete_team():
    team_id = 1
    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.delete(f"/api/team/{team_id}/")
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["message"] == "Team deleted successfully."


@pytest.mark.anyio(asynclib_name="asyncio")
async def test_assign_employee_to_team():
    team_data = t.ConnectionTeamEmployee(
        team_id=5,
        employee_id=3,
        assigned_fte=0.2,
    )
    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.post("/api/team/employee/", json=team_data.model_dump())
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["message"] == "Employees assigned to team successfully"


@pytest.mark.anyio(asynclib_name="asyncio")
async def test_delete_employee_from_team():
    team_data = t.ConnectionTeamEmployee(
        team_id=3,
        employee_id=5,
        assigned_fte=0.4,
    )
    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.delete("/api/team/employee/", params=team_data.model_dump())
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["message"] == "Employee deleted from team successfully."
