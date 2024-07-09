import jwt
import ORM.tables as t
from jwt import ExpiredSignatureError, InvalidTokenError
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import aliased
from sqlalchemy import or_
from typing import List, Optional
from ORM.mapper import Mapper
from helper import Helper as h
from contextlib import asynccontextmanager

m = Mapper()
m_login = Mapper()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await m.reflect_tables()
    await m_login.reflect_tables(schema="login")
    try:
        yield
    finally:
        await m.engine.dispose()
        await m_login.engine.dispose()


app = FastAPI(lifespan=lifespan)

# API endpoints


# Search
@app.post("/api/search/")
async def search_function(
    data: Optional[List[t.SearchCriteria]] = None,
    db: AsyncSession = Depends(m.get_db_session),
):
    """
    Searches for employees based on the given criteria.
    :param data: List of SearchCriteria objects.
    :param db: The database session.
    :return: List of employees that match the criteria.
    """
    Employee = m.Base.classes.employee
    ExperienceLevel = m.Base.classes.experience_level
    Type = m.Base.classes.type
    Department = m.Base.classes.department
    Project = m.Base.classes.project
    Team = m.Base.classes.team
    Job = m.Base.classes.job
    Skill = m.Base.classes.skill
    ConnectionTeamEmployee = m.Base.classes.connection_team_employee
    Internal = m.Base.classes.internal
    External = m.Base.classes.external
    ConnectionJobSkill = m.Base.classes.connection_job_skill

    Job_Internal_1 = aliased(Job)
    Job_Internal_2 = aliased(Job)
    Job_External_1 = aliased(Job)
    Job_External_2 = aliased(Job)
    ConnectionJobSkillExternal = aliased(ConnectionJobSkill)
    ConnectionJobSkillInternal = aliased(ConnectionJobSkill)
    Skill_Internal = aliased(Skill)
    Skill_External = aliased(Skill)
    ConnectionTeamEmployee_1 = aliased(ConnectionTeamEmployee)
    ConnectionTeamEmployee_2 = aliased(ConnectionTeamEmployee)
    Team_1 = aliased(Team)
    Team_2 = aliased(Team)
    Project_1 = aliased(Project)
    Project_2 = aliased(Project)
    Internal_1 = aliased(Internal)
    Internal_2 = aliased(Internal)
    External_1 = aliased(External)
    External_2 = aliased(External)

    query = (
        select(
            Employee.employee_id,
            Employee.first_name,
            Employee.last_name,
            Employee.free_fte,
            Employee.e_mail,
            Employee.phone_number,
            Employee.entry_date,
            ExperienceLevel.exp_lvl_description,
            Type.type_name,
            ExperienceLevel.exp_lvl_description,
        )
        .join(
            ExperienceLevel,
            Employee.experience_level_id == ExperienceLevel.experience_level_id,
        )
        .join(Type, Employee.type_id == Type.type_id)
    )

    if data is not None:
        for criteria in data:
            if criteria.department is not None:
                query = (
                    query.join(
                        ConnectionTeamEmployee_1,
                        Employee.employee_id == ConnectionTeamEmployee_1.employee_id,
                    )
                    .join(Team_1, ConnectionTeamEmployee_1.team_id == Team_1.team_id)
                    .join(Project_1, Team_1.project_id == Project_1.project_id)
                    .join(
                        Department, Project_1.department_id == Department.department_id
                    )
                    .filter(Department.dep_name == criteria.department)
                )

            if criteria.job is not None:
                query = (
                    query.join(
                        Internal_1,
                        Employee.employee_id == Internal_1.employee_id,
                        isouter=True,
                    )
                    .join(
                        Job_Internal_1,
                        Internal_1.job_id == Job_Internal_1.job_id,
                        isouter=True,
                    )
                    .join(
                        External_1,
                        Employee.employee_id == External_1.employee_id,
                        isouter=True,
                    )
                    .join(
                        Job_External_1,
                        External_1.job_id == Job_External_1.job_id,
                        isouter=True,
                    )
                    .filter(
                        or_(
                            Job_Internal_1.job_name == criteria.job,
                            Job_External_1.job_name == criteria.job,
                        )
                    )
                )

            if criteria.experienceLevel is not None:
                query = query.filter(
                    ExperienceLevel.exp_lvl_description == criteria.experienceLevel
                )

            if criteria.project is not None:
                query = (
                    query.join(
                        ConnectionTeamEmployee_2,
                        Employee.employee_id == ConnectionTeamEmployee_2.employee_id,
                    )
                    .join(Team_2, ConnectionTeamEmployee_2.team_id == Team_2.team_id)
                    .join(Project_2, Team_2.project_id == Project_2.project_id)
                    .filter(Project_2.proj_name == criteria.project)
                )

            if criteria.type is not None:
                query = query.filter(Type.type_name == criteria.type)

            if criteria.skill is not None:
                query = (
                    query.join(
                        Internal_2,
                        Employee.employee_id == Internal_2.employee_id,
                        isouter=True,
                    )
                    .join(
                        Job_Internal_2,
                        Internal_2.job_id == Job_Internal_2.job_id,
                        isouter=True,
                    )
                    .join(
                        External_2,
                        Employee.employee_id == External_2.employee_id,
                        isouter=True,
                    )
                    .join(
                        Job_External_2,
                        External_2.job_id == Job_External_2.job_id,
                        isouter=True,
                    )
                    .join(
                        ConnectionJobSkillInternal,
                        Job_Internal_2.job_id == ConnectionJobSkillInternal.job_id,
                        isouter=True,
                    )
                    .join(
                        ConnectionJobSkillExternal,
                        Job_External_2.job_id == ConnectionJobSkillExternal.job_id,
                        isouter=True,
                    )
                    .join(
                        Skill_Internal,
                        ConnectionJobSkillInternal.skill_id == Skill_Internal.skill_id,
                        isouter=True,
                    )
                    .join(
                        Skill_External,
                        ConnectionJobSkillExternal.skill_id == Skill_External.skill_id,
                        isouter=True,
                    )
                    .filter(
                        or_(
                            Skill_Internal.skill_name == criteria.skill,
                            Skill_External.skill_name == criteria.skill,
                        )
                    )
                )

            if criteria.fte is not None:
                query = query.filter(Employee.free_fte >= criteria.fte)

    result = await db.execute(query)

    db.expire_all()

    employees = [
        {
            "employee_id": row.employee_id,
            "first_name": row.first_name,
            "last_name": row.last_name,
            "free_fte": row.free_fte,
            "e_mail": row.e_mail,
            "phone_number": row.phone_number,
            "entry_date": row.entry_date,
            "exp_lvl_description": row.exp_lvl_description,
            "type_name": row.type_name,
        }
        for row in result.mappings().all()
    ]

    return {"employee": employees}


# CRUD operations for the employee table
@app.get("/api/employee/")
async def get_employee(db: AsyncSession = Depends(m.get_db_session)):
    """
    Returns all employees.
    :param db: The database session.
    :return: List of all employees.
    """
    Employee = m.Base.classes.employee
    Exp_Level = m.Base.classes.experience_level
    Type = m.Base.classes.type

    result = await db.execute(
        select(
            Employee.employee_id,
            Employee.first_name,
            Employee.last_name,
            Employee.free_fte,
            Employee.e_mail,
            Employee.phone_number,
            Employee.entry_date,
            Exp_Level.exp_lvl_description,
            Type.type_name,
        )
        .join(Exp_Level, Employee.experience_level_id == Exp_Level.experience_level_id)
        .join(Type, Employee.type_id == Type.type_id)
    )
    db.expire_all()

    employees = [
        {
            "employee_id": row.employee_id,
            "first_name": row.first_name,
            "last_name": row.last_name,
            "free_fte": row.free_fte,
            "e_mail": row.e_mail,
            "phone_number": row.phone_number,
            "entry_date": row.entry_date,
            "exp_lvl_description": row.exp_lvl_description,
            "type_name": row.type_name,
        }
        for row in result.mappings().all()
    ]

    return {"employee": employees}


@app.get("/api/employee/{employee_id}/")
async def get_employee_by_id(
    employee_id: int, db: AsyncSession = Depends(m.get_db_session)
):
    """
    Returns an employee by given ID.
    :param employee_id: The ID of the employee to return.
    :param db: The database session.
    :return: The employee with the given ID.
    """
    Employee = m.Base.classes.employee
    Exp_Level = m.Base.classes.experience_level
    Type = m.Base.classes.type

    result = await db.execute(
        select(
            Employee.employee_id,
            Employee.first_name,
            Employee.last_name,
            Employee.free_fte,
            Employee.e_mail,
            Employee.phone_number,
            Employee.entry_date,
            Exp_Level.exp_lvl_description,
            Type.type_name,
            Employee.address_id,
        )
        .join(Exp_Level, Employee.experience_level_id == Exp_Level.experience_level_id)
        .join(Type, Employee.type_id == Type.type_id)
        .where(Employee.employee_id == employee_id)
    )
    db.expire_all()

    employee = [
        {
            "employee_id": row.employee_id,
            "first_name": row.first_name,
            "last_name": row.last_name,
            "free_fte": row.free_fte,
            "e_mail": row.e_mail,
            "phone_number": row.phone_number,
            "entry_date": row.entry_date,
            "exp_lvl_description": row.exp_lvl_description,
            "type_name": row.type_name,
            "address_id": row.address_id,
        }
        for row in result.mappings().all()
    ]

    return {"employee": employee}


@app.delete("/api/employee/{employee_id}/")
async def delete_employee(
    employee_id: int, db: AsyncSession = Depends(m.get_db_session)
):
    """
    Deletes an employee by given ID.
    :param employee_id: The ID of the employee to delete.
    :param db: The database session.
    :return: Success message if the employee was successfully deleted, error message otherwise.
    """
    Employee = m.Base.classes.employee
    ConnectionTeamEmployee = m.Base.classes.connection_team_employee
    Project = m.Base.classes.project
    Team = m.Base.classes.team
    operation = "delete"

    team_fte = await db.execute(
        select(ConnectionTeamEmployee.assigned_fte, Team.project_id)
        .filter(ConnectionTeamEmployee.employee_id == employee_id)
        .join(Team, ConnectionTeamEmployee.team_id == Team.team_id)
    )

    try:
        for projects in team_fte.mappings().all():
            entity_project = await db.get(Project, projects.project_id)
            if not entity_project:
                raise Exception("Could not find project")

            if hasattr(entity_project, "current_fte"):
                new_fte = await h.calculate_project_fte(
                    Project, projects.project_id, projects.assigned_fte, operation, db
                )
                setattr(entity_project, "current_fte", new_fte)

        deletion_successful = await h.universal_delete(Employee, db, employee_id=employee_id)

        if deletion_successful:
            await db.commit()
            return {"status": "success", "message": "Employee deleted successfully."}
        else:
            raise Exception("Employee not found")

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting employee: {e}")


@app.post("/api/employee/")
async def create_employees(
    employee_data: t.Employee, db: AsyncSession = Depends(m.get_db_session)
):
    """
    Creates a new employees.
    :param employee_data: List of Employee attributes.
    :param db: The database session.
    :return: Success message if the employee was successfully created, error message otherwise.
    """
    Employee = m.Base.classes.employee

    if 0 < employee_data.base_fte <= 1:
        new_employee = Employee(**employee_data.model_dump())
        db.add(new_employee)
    else:
        await db.rollback()
        raise Exception("Error false FTE")
    try:
        await db.commit()
        return {"message": "Employees created successfully"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating employee: {e}")


@app.put("/api/employee/{employee_id}/")
async def update_employee(
    employee_id: int,
    update_data: t.Employee,
    db: AsyncSession = Depends(m.get_db_session),
):
    """
    Updates an employee by given ID.
    :param employee_id: The ID of the employee to update.
    :param update_data: The data to update.
    :param db: The database session.
    :return: Success message if the employee was successfully updated, error message otherwise.
    """
    Employee = m.Base.classes.employee

    fte_result = await db.execute(
        select(
            Employee.base_fte,
            Employee.free_fte
        )
        .filter(Employee.employee_id == employee_id)
    )

    for fte_row in fte_result.mappings().all():
        free_fte = fte_row.free_fte
        base_fte = fte_row.base_fte

    new_base_fte = update_data.base_fte
    assigned_fte = base_fte - free_fte

    if not (0.0 < new_base_fte <= 1):
        raise HTTPException(
            status_code=400, detail="Error updating employee: False FTE"
        )

    elif not new_base_fte >= assigned_fte:
        raise HTTPException(
            status_code=400, detail="Error updating employee: Base FTE too low"
        )

    new_free_fte = new_base_fte - assigned_fte
    update_data.free_fte = new_free_fte

    try:
        update_successful = await h.universal_update(
            Employee, db, employee_id, update_data
        )
        if update_successful:
            return {"status": "success", "message": "Employee updated successfully."}
        else:
            raise HTTPException(status_code=404, detail="Employee not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating employee: {e}")


# Read operation for internal, external and stat table
@app.get("/api/internal/")
async def get_internal(db: AsyncSession = Depends(m.get_db_session)):
    """
    Returns all internal employees.
    :param db: The database session.
    :return: List of all internal employees.
    """
    Employee = m.Base.classes.employee
    Exp_Level = m.Base.classes.experience_level
    Type = m.Base.classes.type

    result = await db.execute(
        select(
            Employee.employee_id,
            Employee.first_name,
            Employee.last_name,
            Employee.free_fte,
            Employee.e_mail,
            Employee.phone_number,
            Employee.entry_date,
            Exp_Level.exp_lvl_description,
            Type.type_name,
        )
        .join(Exp_Level, Employee.experience_level_id == Exp_Level.experience_level_id)
        .join(Type, Employee.type_id == Type.type_id)
        .where(Employee.type_id == 1)
    )
    db.expire_all()

    internals = [
        {
            "employee_id": row.employee_id,
            "first_name": row.first_name,
            "last_name": row.last_name,
            "free_fte": row.free_fte,
            "e_mail": row.e_mail,
            "phone_number": row.phone_number,
            "entry_date": row.entry_date,
            "exp_lvl_description": row.exp_lvl_description,
            "type_name": row.type_name,
        }
        for row in result.mappings().all()
    ]

    return {"internal": internals}


@app.get("/api/external/")
async def get_external(db: AsyncSession = Depends(m.get_db_session)):
    """
    Returns all external employees.
    :param db: The database session.
    :return: List of all external employees.
    """
    Employee = m.Base.classes.employee
    Exp_Level = m.Base.classes.experience_level
    Type = m.Base.classes.type

    result = await db.execute(
        select(
            Employee.employee_id,
            Employee.first_name,
            Employee.last_name,
            Employee.free_fte,
            Employee.e_mail,
            Employee.phone_number,
            Employee.entry_date,
            Exp_Level.exp_lvl_description,
            Type.type_name,
        )
        .join(Exp_Level, Employee.experience_level_id == Exp_Level.experience_level_id)
        .join(Type, Employee.type_id == Type.type_id)
        .where(Employee.type_id == 2)
    )
    db.expire_all()

    externals = [
        {
            "employee_id": row.employee_id,
            "first_name": row.first_name,
            "last_name": row.last_name,
            "free_fte": row.free_fte,
            "e_mail": row.e_mail,
            "phone_number": row.phone_number,
            "entry_date": row.entry_date,
            "exp_lvl_description": row.exp_lvl_description,
            "type_name": row.type_name,
        }
        for row in result.mappings().all()
    ]

    return {"external": externals}


@app.get("/api/stat/")
async def get_stat(db: AsyncSession = Depends(m.get_db_session)):
    """
    Returns all stats.
    :param db: The database session.
    :return: List of all stats.
    """
    Employee = m.Base.classes.employee
    Exp_Level = m.Base.classes.experience_level
    Type = m.Base.classes.type

    result = await db.execute(
        select(
            Employee.employee_id,
            Employee.first_name,
            Employee.last_name,
            Employee.free_fte,
            Employee.e_mail,
            Employee.phone_number,
            Employee.entry_date,
            Exp_Level.exp_lvl_description,
            Type.type_name,
        )
        .join(Exp_Level, Employee.experience_level_id == Exp_Level.experience_level_id)
        .join(Type, Employee.type_id == Type.type_id)
        .where(Employee.type_id == 3)
    )
    db.expire_all()

    stats = [
        {
            "employee_id": row.employee_id,
            "first_name": row.first_name,
            "last_name": row.last_name,
            "free_fte": row.free_fte,
            "e_mail": row.e_mail,
            "phone_number": row.phone_number,
            "entry_date": row.entry_date,
            "exp_lvl_description": row.exp_lvl_description,
            "type_name": row.type_name,
        }
        for row in result.mappings().all()
    ]

    return {"stat": stats}


# CRUD operations for the project table
@app.get("/api/project/")
async def get_project(db: AsyncSession = Depends(m.get_db_session)):
    """
    Returns all projects.
    :param db: The database session.
    :return: List of all projects.
    """
    Project = m.Base.classes.project
    Department = m.Base.classes.department
    Employee = m.Base.classes.employee

    result = await db.execute(
        select(
            Project.project_id,
            Project.proj_name.label("project_name"),
            Department.dep_name.label("department_name"),
            Employee.last_name.label("supervisor_last_name"),
            Project.proj_priority,
            Project.needed_fte,
            Project.current_fte,
            Project.start_date,
            Project.end_date,
        )
        .join(Department, Project.department_id == Department.department_id)
        .join(Employee, Project.proj_manager == Employee.employee_id)
    )
    db.expire_all()

    projects = [
        {
            "project_id": row.project_id,
            "project_name": row.project_name,
            "department_name": row.department_name,
            "supervisor": row.supervisor_last_name,
            "proj_priority": row.proj_priority,
            "needed_fte": row.needed_fte,
            "current_fte": row.current_fte,
            "start_date": row.start_date.isoformat() if row.start_date else None,
            "end_date": row.end_date.isoformat() if row.end_date else None,
        }
        for row in result.mappings().all()
    ]

    return {"project": projects}


@app.get("/api/project/{project_id}/")
async def get_project_by_id(
    project_id: int, db: AsyncSession = Depends(m.get_db_session)
):
    """
    Returns a project by given ID.
    :param project_id: The ID of the project to return.
    :param db: The database session.
    :return: The project with the given ID.
    """
    Project = m.Base.classes.project
    Department = m.Base.classes.department
    Employee = m.Base.classes.employee

    result = await db.execute(
        select(
            Project.project_id,
            Project.proj_name.label("project_name"),
            Department.dep_name.label("department_name"),
            Employee.last_name.label("supervisor_last_name"),
            Project.proj_priority,
            Project.needed_fte,
            Project.current_fte,
            Project.start_date,
            Project.end_date,
        )
        .join(Department, Project.department_id == Department.department_id)
        .join(Employee, Project.proj_manager == Employee.employee_id)
        .where(Project.project_id == project_id)
    )
    db.expire_all()

    project = [
        {
            "project_id": row.project_id,
            "project_name": row.project_name,
            "department_name": row.department_name,
            "supervisor": row.supervisor_last_name,
            "proj_priority": row.proj_priority,
            "needed_fte": row.needed_fte,
            "current_fte": row.current_fte,
            "start_date": row.start_date.isoformat() if row.start_date else None,
            "end_date": row.end_date.isoformat() if row.end_date else None,
        }
        for row in result.mappings().all()
    ]

    return {"project": project}


@app.delete("/api/project/{project_id}/")
async def delete_project(project_id: int, db: AsyncSession = Depends(m.get_db_session)):
    """
    Deletes a project by given ID.
    :param project_id: The ID of the project to delete.
    :param db: The database session.
    :return: Success message if the project was successfully deleted, error message otherwise.
    """
    Employee = m.Base.classes.employee
    ConnectionTeamEmployee = m.Base.classes.connection_team_employee
    Project = m.Base.classes.project
    Team = m.Base.classes.team
    operation = "delete"

    employee_fte = await db.execute(
        select(ConnectionTeamEmployee.assigned_fte, ConnectionTeamEmployee.employee_id)
        .join(Team, ConnectionTeamEmployee.team_id == Team.team_id)
        .filter(Team.project_id == project_id)
    )

    try:
        for employees in employee_fte.mappings().all():
            entity_employee = await db.get(Employee, employees.employee_id)
            if not entity_employee:
                raise Exception("Could not find employee")
            
            if hasattr(entity_employee, "free_fte"):
                new_fte = await h.calculate_employee_fte(
                    Employee, employees.employee_id, employees.assigned_fte, operation, db
                )
                setattr(entity_employee, "free_fte", new_fte)

        deletion_successful = await h.universal_delete(
            Project, db, project_id=project_id
        )

        if deletion_successful:
            await db.commit()
            return {"status": "success", "message": "Project deleted successfully."}
        else:
            raise HTTPException(status_code=404, detail="Project not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting project: {e}")


@app.post("/api/project/")
async def create_project(
    project_data: t.Project, db: AsyncSession = Depends(m.get_db_session)
):
    """
    Creates a new project.
    :param project_data: List of Project attributes.
    :param db: The database session.
    :return: Success message if the project was successfully created, error message otherwise.
    """
    Project = m.Base.classes.project

    new_project = Project(**project_data.model_dump())
    if not (0.0 <= new_project.needed_fte):
        await db.rollback()
        raise HTTPException(
            status_code=400, detail="Error assigning needed FTE to project: False FTE"
        )
    db.add(new_project)
    try:
        await db.commit()
        new_project_id = new_project.project_id
        return {"message": "Project created successfully", "Project ID": new_project_id}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating project: {e}")


@app.put("/api/project/{project_id}/")
async def update_project(
    project_id: int,
    update_data: t.Project,
    db: AsyncSession = Depends(m.get_db_session),
):
    """
    Updates a project by given ID.
    :param project_id: The ID of the project to update.
    :param update_data: The data to update.
    :param db: The database session.
    :return: Success message if the project was successfully updated, error message otherwise.
    """
    Project = m.Base.classes.project

    new_needed_fte = update_data.needed_fte

    fte_result = await db.execute(
        select(
            Project.current_fte
        )
        .filter(Project.project_id == project_id)
    )

    for fte_row in fte_result.mappings().all():
        current_fte = fte_row.current_fte

    if not (0.0 < new_needed_fte):
        raise HTTPException(
            status_code=400, detail="Error updating project: False FTE"
        )

    elif not new_needed_fte >= current_fte:
        raise HTTPException(
            status_code=400, detail="Error updating project: Needed FTE too low"
        )    
    
    try:
        update_successful = await h.universal_update(
            Project, db, project_id, update_data
        )
        if update_successful:
            return {"status": "success", "message": "Project updated successfully."}
        else:
            raise Exception("Project not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating project: {e}")


@app.get("/api/project/employee/{project_id}/")
async def search_project_employee(
    project_id: int, db: AsyncSession = Depends(m.get_db_session)
):
    """
    Searches for employees that are assigned to a given project.
    :param project_id: The ID of the project to search for.
    :param db: The database session.
    :return: List of employees that are assigned to the given project.
    """
    Project = m.Base.classes.project
    Employee = m.Base.classes.employee
    Team = m.Base.classes.team
    Exp_Level = m.Base.classes.experience_level
    Type = m.Base.classes.type
    ConnectionTeamEmployee = m.Base.classes.connection_team_employee

    result = await db.execute(
        select(
            Employee.employee_id,
            Employee.first_name,
            Employee.last_name,
            Employee.free_fte,
            Employee.e_mail,
            Employee.phone_number,
            Employee.entry_date,
            Exp_Level.exp_lvl_description,
            Type.type_name,
            Team.team_name,
        )
        .join(
            ConnectionTeamEmployee,
            Employee.employee_id == ConnectionTeamEmployee.employee_id,
        )
        .join(Team, ConnectionTeamEmployee.team_id == Team.team_id)
        .join(Project, Team.project_id == Project.project_id)
        .join(Exp_Level, Employee.experience_level_id == Exp_Level.experience_level_id)
        .join(Type, Employee.type_id == Type.type_id)
        .filter(Project.project_id == project_id)
    )
    db.expire_all()

    employees = [
        {
            "employee_id": row.employee_id,
            "first_name": row.first_name,
            "last_name": row.last_name,
            "free_fte": row.free_fte,
            "e_mail": row.e_mail,
            "phone_number": row.phone_number,
            "entry_date": row.entry_date,
            "exp_lvl_description": row.exp_lvl_description,
            "type_name": row.type_name,
            "team_name": row.team_name,
        }
        for row in result.mappings().all()
    ]

    return {"employee": employees}


@app.get("/api/project/team/{project_id}/")
async def search_project_team(
    project_id: int, db: AsyncSession = Depends(m.get_db_session)
):
    """
    Searches for teams that are assigned to a given project.
    :param project_id: The ID of the project to search for.
    :param db: The database session.
    :return: List of teams that are assigned to the given project.
    """
    Project = m.Base.classes.project
    Team = m.Base.classes.team

    result = await db.execute(
        select(Team.team_id, Team.team_name, Team.team_purpose)
        .join(Project, Team.project_id == Project.project_id)
        .filter(Project.project_id == project_id)
    )
    db.expire_all()

    teams = [
        {
            "team_id": row.team_id,
            "team_name": row.team_name,
            "team_purpose": row.team_purpose,
        }
        for row in result.mappings().all()
    ]

    return {"team": teams}


# CRUD operations for team table
@app.get("/api/team/")
async def get_team(db: AsyncSession = Depends(m.get_db_session)):
    """
    Returns all teams.
    :param db: The database session.
    :return: List of all teams.
    """
    Team = m.Base.classes.team
    Project = m.Base.classes.project

    result = await db.execute(
        select(Team.team_id, Team.team_name, Team.team_purpose, Project.proj_name).join(
            Project, Team.project_id == Project.project_id
        )
    )
    db.expire_all()

    teams = [
        {
            "team_id": row.team_id,
            "team_name": row.team_name,
            "team_purpose": row.team_purpose,
            "project_name": row.proj_name,
        }
        for row in result.mappings().all()
    ]

    return {"team": teams}


@app.get("/api/team/{team_id}/")
async def get_team_by_id(team_id: int, db: AsyncSession = Depends(m.get_db_session)):
    """
    Returns a team by given ID.
    :param team_id: The ID of the team to return.
    :param db: The database session.
    :return: The team with the given ID.
    """
    Team = m.Base.classes.team
    Project = m.Base.classes.project

    result = await db.execute(
        select(Team.team_id, Team.team_name, Team.team_purpose, Project.proj_name)
        .join(Project, Team.project_id == Project.project_id)
        .where(Team.team_id == team_id)
    )
    db.expire_all()

    team = [
        {
            "team_id": row.team_id,
            "team_name": row.team_name,
            "team_purpose": row.team_purpose,
            "project_name": row.proj_name,
        }
        for row in result.mappings().all()
    ]

    return {"team": team}


@app.delete("/api/team/{team_id}/")
async def delete_team(team_id: int, db: AsyncSession = Depends(m.get_db_session)):
    """
    NOTE: Not used by GUI at this moment!
    Deletes a team by given ID.
    :param team_id: The ID of the team to delete.
    :param db: The database session.
    :return: Success message if the team was successfully deleted, error message otherwise.
    """
    Team = m.Base.classes.team
    ConnectionTeamEmployee = m.Base.classes.connection_team_employee
    try:
        deletion_successful = await h.universal_delete(Team, db, team_id=team_id)
        deletion_casc_connection = await h.universal_delete(
            ConnectionTeamEmployee, db, team_id=team_id
        )
        if deletion_successful and deletion_casc_connection:
            return {"status": "success", "message": "Team deleted successfully."}
        else:
            raise HTTPException(status_code=404, detail="Team not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting team: {e}")


@app.post("/api/team/")
async def create_team(team_data: t.Team, db: AsyncSession = Depends(m.get_db_session)):
    """
    Creates a new team.
    :param team_data: List of Team attributes.
    :param db: The database session.
    :return: Success message if the team was successfully created, error message otherwise.
    """
    Team = m.Base.classes.team

    new_team = Team(**team_data.model_dump())
    db.add(new_team)
    try:
        await db.commit()
        return {"message": "Team created successfully"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating team: {e}")


@app.put("/api/team/{team_id}/")
async def update_team(
    team_id: int, update_data: t.Team, db: AsyncSession = Depends(m.get_db_session)
):
    """
    Updates a team by given ID.
    NOTE: Not used by GUI at this moment!
    :param team_id: The ID of the team to update.
    :param update_data: The data to update.
    :param db: The database session.
    :return: Success message if the team was successfully updated, error message otherwise.
    """
    Team = m.Base.classes.team

    try:
        update_successful = await h.universal_update(Team, db, team_id, update_data)
        if update_successful:
            return {"status": "success", "message": "Team updated successfully."}
        else:
            raise HTTPException(status_code=404, detail="Team not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating team: {e}")


@app.get("/api/team/employee/{team_id}/")
async def search_team_employee(
    team_id: int, db: AsyncSession = Depends(m.get_db_session)
):
    """
    Searches for employees that are assigned to a given team.
    :param team_id: The ID of the team to search for.
    :param db: The database session.
    :return: List of employees that are assigned to the given team.
    """
    Team = m.Base.classes.team
    Employee = m.Base.classes.employee
    Exp_Level = m.Base.classes.experience_level
    Type = m.Base.classes.type
    ConnectionTeamEmployee = m.Base.classes.connection_team_employee

    result = await db.execute(
        select(
            Employee.employee_id,
            Employee.first_name,
            Employee.last_name,
            Employee.free_fte,
            Employee.e_mail,
            Employee.phone_number,
            Employee.entry_date,
            Exp_Level.exp_lvl_description,
            Type.type_name,
        )
        .join(
            ConnectionTeamEmployee,
            Employee.employee_id == ConnectionTeamEmployee.employee_id,
        )
        .join(Team, ConnectionTeamEmployee.team_id == Team.team_id)
        .join(Exp_Level, Employee.experience_level_id == Exp_Level.experience_level_id)
        .join(Type, Employee.type_id == Type.type_id)
        .filter(Team.team_id == team_id)
    )
    db.expire_all()

    employees = [
        {
            "employee_id": row.employee_id,
            "first_name": row.first_name,
            "last_name": row.last_name,
            "free_fte": row.free_fte,
            "e_mail": row.e_mail,
            "phone_number": row.phone_number,
            "entry_date": row.entry_date,
            "exp_lvl_description": row.exp_lvl_description,
            "type_name": row.type_name,
        }
        for row in result.mappings().all()
    ]

    return {"employee": employees}

# Operations for assigning employees to teams and removing employees from teams
@app.post("/api/team/employee/")
async def assign_employee_to_team(
    team_data: t.ConnectionTeamEmployee, db: AsyncSession = Depends(m.get_db_session)
):
    """
    Assigns an employee to a team.
    :param team_data: List of the team, employee ID and the FTE amount.
    :param db: The database session.
    :return: Success message if the employee was successfully assigned to the team, error message otherwise.
    """
    Employee = m.Base.classes.employee
    Team = m.Base.classes.team
    Project = m.Base.classes.project
    ConnectionTeamEmployee = m.Base.classes.connection_team_employee
    operation = "add"

    new_connection = ConnectionTeamEmployee(**team_data.model_dump())

    if not (0.0 < new_connection.assigned_fte <= 1.0):
        raise HTTPException(
            status_code=400, detail="Error assigning employee to team: False FTE"
        )

    result = await db.execute(
        select(ConnectionTeamEmployee.employee_id)
        .filter(ConnectionTeamEmployee.team_id == new_connection.team_id)
        .filter(ConnectionTeamEmployee.employee_id == new_connection.employee_id)
    )

    result_project_id = await db.execute(
        select(Team.project_id).filter(Team.team_id == new_connection.team_id)
    )

    for result_project_id_row in result_project_id:
        project_id = result_project_id_row.project_id

    try:
        new_employee_fte = await h.calculate_employee_fte(
            Employee,
            new_connection.employee_id,
            new_connection.assigned_fte,
            operation,
            db,
        )
        new_project_fte = await h.calculate_project_fte(
            Project, project_id, new_connection.assigned_fte, operation, db
        )
        entity_employee = await db.get(Employee, new_connection.employee_id)
        if not entity_employee:
            raise HTTPException(status_code=400, detail="Employee Enitity missing")
        entity_project = await db.get(Project, project_id)
        if not entity_project:
            raise HTTPException(status_code=400, detail="Project Enitity missing")

        for row in result.mappings().all():
            if row is not None:
                raise HTTPException(
                    status_code=400,
                    detail="Error assigning employee to team: Employee already assigned to team",
                )
        db.add(new_connection)

        if hasattr(entity_employee, "free_fte") and hasattr(
            entity_project, "current_fte"
        ):
            setattr(entity_employee, "free_fte", new_employee_fte)
            setattr(entity_project, "current_fte", new_project_fte)
        await db.commit()
        return {"message": "Employees assigned to team successfully"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Error assigning employees to team: {e}"
        )

        
@app.delete("/api/team/employee/")
async def delete_employee_from_team(
    team_data: t.ConnectionTeamEmployee, db: AsyncSession = Depends(m.get_db_session)
):
    """
    Deletes an employee from a team.
    :param team_data: List of the team and employee ID.
    :param db: The database session.
    :return: Success message if the employee was successfully deleted from the team, error message otherwise.
    """
    Employee = m.Base.classes.employee
    ConnectionTeamEmployee = m.Base.classes.connection_team_employee
    Team = m.Base.classes.team
    Project = m.Base.classes.project

    operation = "delete"

    result_project_id = await db.execute(
        select(Team.project_id).filter(Team.team_id == team_data.team_id)
    )

    for result_project_id_row in result_project_id:
        project_id = result_project_id_row.project_id

    result_assigned_fte = await db.execute(
        select(ConnectionTeamEmployee.assigned_fte)
        .filter(ConnectionTeamEmployee.employee_id == team_data.employee_id)
        .filter(ConnectionTeamEmployee.team_id == team_data.team_id)
    )

    for result_assigned_ftes in result_assigned_fte:
        assigned_fte = result_assigned_ftes.assigned_fte

    try:
        new_employee_fte = await h.calculate_employee_fte(
            Employee,
            team_data.employee_id,
            assigned_fte,
            operation,
            db,
        )
        new_project_fte = await h.calculate_project_fte(
            Project, project_id, assigned_fte, operation, db
        )
        entity_employee = await db.get(Employee, team_data.employee_id)
        if not entity_employee:
            raise Exception("Employee Enitity missing")
        entity_project = await db.get(Project, project_id)
        if not entity_project:
            raise Exception("Project Enitity missing")
        deletion_successful = await h.universal_delete(
            ConnectionTeamEmployee,
            db,
            team_id=team_data.team_id,
            employee_id=team_data.employee_id,
        )

        if not deletion_successful:
            raise HTTPException(status_code=404, detail="Employee not found in team")
        else:
            if hasattr(entity_employee, "free_fte") and hasattr(
                entity_project, "current_fte"
            ):
                setattr(entity_employee, "free_fte", new_employee_fte)
                setattr(entity_project, "current_fte", new_project_fte)
            await db.commit()
            return {
                "status": "success",
                "message": "Employee deleted from team successfully.",
            }

    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error deleting employee from team: {e}"
        )

# Read definition tables (Team, Address, Type, Education Degree, Job, Skill, Experience Level)
@app.get("/api/department/")
async def get_department(db: AsyncSession = Depends(m.get_db_session)):
    """
    Returns all departments.
    :param db: The database session.
    :return: List of all departments.
    """
    Department = m.Base.classes.department
    result = await db.execute(select(Department))
    departments = result.mappings().all()

    return {"department": departments}


@app.get("/api/address/")
async def get_address(db: AsyncSession = Depends(m.get_db_session)):
    """
    Returns all addresses.
    :param db: The database session.
    :return: List of all addresses.
    """
    Address = m.Base.classes.address
    result = await db.execute(select(Address))
    addresses = result.mappings().all()

    return {"address": addresses}


@app.get("/api/type/")
async def get_type(db: AsyncSession = Depends(m.get_db_session)):
    """
    Returns all types.
    :param db: The database session.
    :return: List of all types.
    """
    Type = m.Base.classes.type
    result = await db.execute(select(Type))
    types = result.mappings().all()

    return {"type": types}


@app.get("/api/education_degree/")
async def get_education_degree(db: AsyncSession = Depends(m.get_db_session)):
    """
    Returns all education degrees.
    :param db: The database session.
    :return: List of all education degrees.
    """
    Education_degree = m.Base.classes.education_degree
    result = await db.execute(select(Education_degree))
    edu_degrees = result.mappings().all()

    return {"education_degree": edu_degrees}


@app.get("/api/job/")
async def get_job(db: AsyncSession = Depends(m.get_db_session)):
    """
    Returns all jobs.
    :param db: The database session.
    :return: List of all jobs.
    """
    Job = m.Base.classes.job
    result = await db.execute(select(Job))
    jobs = result.mappings().all()

    return {"job": jobs}


@app.get("/api/skill/")
async def get_skill(db: AsyncSession = Depends(m.get_db_session)):
    """
    Returns all skills.
    :param db: The database session.
    :return: List of all skills.
    """
    Skill = m.Base.classes.skill
    result = await db.execute(select(Skill))
    skills = result.mappings().all()

    return {"skill": skills}


@app.get("/api/experience_level/")
async def get_experience_level(db: AsyncSession = Depends(m.get_db_session)):
    """
    Returns all experience levels.
    :param db: The database session.
    :return: List of all experience levels.
    """
    Experience_level = m.Base.classes.experience_level
    result = await db.execute(select(Experience_level))
    exp_levels = result.mappings().all()

    return {"experience_level": exp_levels}


# Login API
@app.post("/api/login/")
async def login(
    data: t.User_Login, db: AsyncSession = Depends(m_login.get_db_session_login)
):
    """
    Logs in a user.
    :param data: List of the username and password.
    :param db: The database session.
    :return: Success message if the login was successful, error message otherwise. Additionally provides a JWT token if successful.
    """
    Login = m_login.Base.classes.user_login
    result = await db.execute(
        select(Login)
        .where(Login.username == data.username)
        .where(Login.hashed_password == data.password)
    )
    login = result.mappings().first()
    if login is not None:
        token = h.create_jwt(data.username)
        return {"status": "success", "message": "Login successful", "token": token}
    else:
        raise HTTPException(status_code=401, detail="Login failed")


@app.post("/api/verifyToken")
async def verify_token(token: t.Token):
    """
    Verifies a JWT token.
    :param token: The token to verify.
    :return: Success message if the token is valid, error message otherwise.
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.access_token, h.SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
        return {"status": "success", "message": "Token is valid"}
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except InvalidTokenError:
        raise credentials_exception
