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

m = Mapper()
m_login = Mapper()
app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await m.reflect_tables()
    await m_login.reflect_tables(schema="login")


@app.on_event("shutdown")
async def shutdown_event():
    await m.engine.dispose()
    await m_login.engine.dispose()


# API endpoints

# Search for employees based on given criteria
@app.post("/api/search/")
async def search_function(data: Optional[List[t.SearchCriteria]] = None, db: AsyncSession = Depends(m.get_db_session)):
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

    query = (select(
        Employee.employee_id,
        Employee.first_name,
        Employee.last_name,
        Employee.free_fte,
        Employee.e_mail,
        Employee.phone_number,
        Employee.entry_date,
        ExperienceLevel.exp_lvl_description,
        Type.type_name,
        ExperienceLevel.exp_lvl_description
    )
             .join(ExperienceLevel, Employee.experience_level_id == ExperienceLevel.experience_level_id)
             .join(Type, Employee.type_id == Type.type_id)
             )

    if data is not None:
        for criteria in data:
            if criteria.department is not None:
                query = query \
                    .join(ConnectionTeamEmployee_1, Employee.employee_id == ConnectionTeamEmployee_1.employee_id) \
                    .join(Team_1, ConnectionTeamEmployee_1.team_id == Team_1.team_id) \
                    .join(Project_1, Team_1.project_id == Project_1.project_id) \
                    .join(Department, Project_1.department_id == Department.department_id) \
                    .filter(Department.dep_name == criteria.department)

            if criteria.job is not None:
                query = query \
                    .join(Internal_1, Employee.employee_id == Internal_1.employee_id, isouter=True) \
                    .join(Job_Internal_1, Internal_1.job_id == Job_Internal_1.job_id, isouter=True) \
                    .join(External_1, Employee.employee_id == External_1.employee_id, isouter=True) \
                    .join(Job_External_1, External_1.job_id == Job_External_1.job_id, isouter=True) \
                    .filter(or_(
                    Job_Internal_1.job_name == criteria.job,
                    Job_External_1.job_name == criteria.job
                ))

            if criteria.experienceLevel is not None:
                query = query \
                    .filter(ExperienceLevel.exp_lvl_description == criteria.experienceLevel)

            if criteria.project is not None:
                query = query \
                    .join(ConnectionTeamEmployee_2, Employee.employee_id == ConnectionTeamEmployee_2.employee_id) \
                    .join(Team_2, ConnectionTeamEmployee_2.team_id == Team_2.team_id) \
                    .join(Project_2, Team_2.project_id == Project_2.project_id) \
                    .filter(Project_2.proj_name == criteria.project)

            if criteria.type is not None:
                query = query \
                    .filter(Type.type_name == criteria.type)

            if criteria.skill is not None:
                query = query \
                    .join(Internal_2, Employee.employee_id == Internal_2.employee_id, isouter=True) \
                    .join(Job_Internal_2, Internal_2.job_id == Job_Internal_2.job_id, isouter=True) \
                    .join(External_2, Employee.employee_id == External_2.employee_id, isouter=True) \
                    .join(Job_External_2, External_2.job_id == Job_External_2.job_id, isouter=True) \
                    .join(ConnectionJobSkillInternal, Job_Internal_2.job_id == ConnectionJobSkillInternal.job_id,
                          isouter=True) \
                    .join(ConnectionJobSkillExternal, Job_External_2.job_id == ConnectionJobSkillExternal.job_id,
                          isouter=True) \
                    .join(Skill_Internal, ConnectionJobSkillInternal.skill_id == Skill_Internal.skill_id, isouter=True) \
                    .join(Skill_External, ConnectionJobSkillExternal.skill_id == Skill_External.skill_id, isouter=True) \
                    .filter(or_(
                    Skill_Internal.skill_name == criteria.skill,
                    Skill_External.skill_name == criteria.skill
                ))

            if criteria.fte is not None:
                query = query.filter(Employee.free_fte >= criteria.fte)

    result = await db.execute(query)

    db.expire_all()

    employees = [{
        'employee_id': row.employee_id,
        'first_name': row.first_name,
        'last_name': row.last_name,
        'free_fte': row.free_fte,
        'e_mail': row.e_mail,
        'phone_number': row.phone_number,
        'entry_date': row.entry_date,
        'exp_lvl_description': row.exp_lvl_description,
        'type_name': row.type_name
    } for row in result.mappings().all()]

    return {"employee": employees}


# delete assignment employees to team
@app.delete("/api/team/employee/")
async def delete_employee_from_team(team_data: t.ConnectionTeamEmployee, db: AsyncSession = Depends(m.get_db_session)):
    ConnectionTeamEmployee = m.Base.classes.connection_team_employee

    try:
        deletion_successful = await h.universal_delete(ConnectionTeamEmployee, db, team_id=team_data.team_id,
                                                       employee_id=team_data.employee_id)
        if deletion_successful:
            return {"status": "success", "message": "Employee deleted from team successfully."}
        else:
            raise HTTPException(status_code=404, detail="Employee not found in team")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting employee from team: {e}")


# CRUD operations for the Employee table
@app.get('/api/employee/')
async def get_employee(db: AsyncSession = Depends(m.get_db_session)):
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
            Type.type_name
        )
        .join(Exp_Level, Employee.experience_level_id == Exp_Level.experience_level_id)
        .join(Type, Employee.type_id == Type.type_id)
    )
    db.expire_all()

    employees = [{
        'employee_id': row.employee_id,
        'first_name': row.first_name,
        'last_name': row.last_name,
        'free_fte': row.free_fte,
        'e_mail': row.e_mail,
        'phone_number': row.phone_number,
        'entry_date': row.entry_date,
        'exp_lvl_description': row.exp_lvl_description,
        'type_name': row.type_name
    } for row in result.mappings().all()]

    return {"employee": employees}


@app.get('/api/employee/{employee_id}/')
async def get_employee_by_id(employee_id: int, db: AsyncSession = Depends(m.get_db_session)):
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
            Employee.address_id
        )
        .join(Exp_Level, Employee.experience_level_id == Exp_Level.experience_level_id)
        .join(Type, Employee.type_id == Type.type_id)
        .where(Employee.employee_id == employee_id)
    )
    db.expire_all()

    employee = [{
        'employee_id': row.employee_id,
        'first_name': row.first_name,
        'last_name': row.last_name,
        'free_fte': row.free_fte,
        'e_mail': row.e_mail,
        'phone_number': row.phone_number,
        'entry_date': row.entry_date,
        'exp_lvl_description': row.exp_lvl_description,
        'type_name': row.type_name,
        'address_id': row.address_id
    } for row in result.mappings().all()]

    return {"employee": employee}


@app.delete("/api/employee/{employee_id}/")
async def delete_employee(employee_id: int, db: AsyncSession = Depends(m.get_db_session)):
    Employee = m.Base.classes.employee
    ConnectionTeamEmployee = m.Base.classes.connection_team_employee
    try:
        deletion_casc_connection = await h.universal_delete(ConnectionTeamEmployee, db, employee_id=employee_id)
        deletion_successful = await h.universal_delete(Employee, db, employee_id=employee_id)
        if deletion_successful and deletion_casc_connection:
            return {"status": "success", "message": "Employee deleted successfully."}
        else:
            raise HTTPException(status_code=404, detail="Employee not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting employee: {e}")


@app.post("/api/employee/")
async def create_employees(employee_data: List[t.Employee], db: AsyncSession = Depends(m.get_db_session)):
    Employee = m.Base.classes.employee

    for data in employee_data:
        new_employee = Employee(**data.dict())
        db.add(new_employee)
    try:
        await db.commit()
        return {"message": "Employees created successfully"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating employee: {e}")


@app.put("/api/employee/{employee_id}/")
async def update_employee(employee_id: int, update_data: t.Employee, db: AsyncSession = Depends(m.get_db_session)):
    Employee = m.Base.classes.employee

    try:
        update_successful = await h.universal_update(Employee, db, employee_id, update_data)
        if update_successful:
            return {"status": "success", "message": "Employee updated successfully."}
        else:
            raise HTTPException(status_code=404, detail="Employee not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating employee: {e}")


# Read Internal, External, Stat employees
@app.get('/api/internal/')
async def get_internal(db: AsyncSession = Depends(m.get_db_session)):
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
            Type.type_name
        )
        .join(Exp_Level, Employee.experience_level_id == Exp_Level.experience_level_id)
        .join(Type, Employee.type_id == Type.type_id)
        .where(Employee.type_id == 1)
    )
    db.expire_all()

    internals = [{
        'employee_id': row.employee_id,
        'first_name': row.first_name,
        'last_name': row.last_name,
        'free_fte': row.free_fte,
        'e_mail': row.e_mail,
        'phone_number': row.phone_number,
        'entry_date': row.entry_date,
        'exp_lvl_description': row.exp_lvl_description,
        'type_name': row.type_name
    } for row in result.mappings().all()]

    return {"internal": internals}


@app.get('/api/external/')
async def get_external(db: AsyncSession = Depends(m.get_db_session)):
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
            Type.type_name
        )
        .join(Exp_Level, Employee.experience_level_id == Exp_Level.experience_level_id)
        .join(Type, Employee.type_id == Type.type_id)
        .where(Employee.type_id == 2)
    )
    db.expire_all()

    externals = [{
        'employee_id': row.employee_id,
        'first_name': row.first_name,
        'last_name': row.last_name,
        'free_fte': row.free_fte,
        'e_mail': row.e_mail,
        'phone_number': row.phone_number,
        'entry_date': row.entry_date,
        'exp_lvl_description': row.exp_lvl_description,
        'type_name': row.type_name
    } for row in result.mappings().all()]

    return {"external": externals}


@app.get('/api/stat/')
async def get_stat(db: AsyncSession = Depends(m.get_db_session)):
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
            Type.type_name
        )
        .join(Exp_Level, Employee.experience_level_id == Exp_Level.experience_level_id)
        .join(Type, Employee.type_id == Type.type_id)
        .where(Employee.type_id == 3)
    )
    db.expire_all()

    stats = [{
        'employee_id': row.employee_id,
        'first_name': row.first_name,
        'last_name': row.last_name,
        'free_fte': row.free_fte,
        'e_mail': row.e_mail,
        'phone_number': row.phone_number,
        'entry_date': row.entry_date,
        'exp_lvl_description': row.exp_lvl_description,
        'type_name': row.type_name
    } for row in result.mappings().all()]

    return {"stat": stats}


# CRUD operations for the Project table
@app.get('/api/project/')
async def get_project(db: AsyncSession = Depends(m.get_db_session)):
    Project = m.Base.classes.project
    Department = m.Base.classes.department
    Employee = m.Base.classes.employee

    result = await db.execute(
        select(
            Project.project_id,
            Project.proj_name.label('project_name'),
            Department.dep_name.label('department_name'),
            Employee.last_name.label('supervisor_last_name'),
            Project.proj_priority,
            Project.needed_fte,
            Project.current_fte,
            Project.start_date,
            Project.end_date
        )
        .join(Department, Project.department_id == Department.department_id)
        .join(Employee, Project.proj_manager == Employee.employee_id)
    )
    db.expire_all()

    projects = [{
        'project_id': row.project_id,
        'project_name': row.project_name,
        'department_name': row.department_name,
        'supervisor': row.supervisor_last_name,
        'proj_priority': row.proj_priority,
        'needed_fte': row.needed_fte,
        'current_fte': row.current_fte,
        'start_date': row.start_date.isoformat() if row.start_date else None,
        'end_date': row.end_date.isoformat() if row.end_date else None
    } for row in result.mappings().all()]

    return {"project": projects}


@app.get('/api/project/{project_id}/')
async def get_project_by_id(project_id: int, db: AsyncSession = Depends(m.get_db_session)):
    Project = m.Base.classes.project
    Department = m.Base.classes.department
    Employee = m.Base.classes.employee
    Team = m.Base.classes.team

    result = await db.execute(
        select(
            Project.project_id,
            Project.proj_name.label('project_name'),
            Department.dep_name.label('department_name'),
            Employee.last_name.label('supervisor_last_name'),
            Project.proj_priority,
            Project.needed_fte,
            Project.current_fte,
            Project.start_date,
            Project.end_date
        )
        .join(Department, Project.department_id == Department.department_id)
        .join(Employee, Project.proj_manager == Employee.employee_id)
        .where(Project.project_id == project_id)
    )
    db.expire_all()

    project = [{
        'project_id': row.project_id,
        'project_name': row.project_name,
        'department_name': row.department_name,
        'supervisor': row.supervisor_last_name,
        'proj_priority': row.proj_priority,
        'needed_fte': row.needed_fte,
        'current_fte': row.current_fte,
        'start_date': row.start_date.isoformat() if row.start_date else None,
        'end_date': row.end_date.isoformat() if row.end_date else None
    } for row in result.mappings().all()]

    return {"project": project}


@app.delete('/api/project/{project_id}/')
async def delete_project(project_id: int, db: AsyncSession = Depends(m.get_db_session)):
    Project = m.Base.classes.project
    try:
        deletion_successful = await h.universal_delete(Project, db, project_id=project_id)
        if deletion_successful:
            return {"status": "success", "message": "Project deleted successfully."}
        else:
            raise HTTPException(status_code=404, detail="Project not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting project: {e}")


@app.post('/api/project/')
async def create_project(project_data: List[t.Project], db: AsyncSession = Depends(m.get_db_session)):
    Project = m.Base.classes.project

    for data in project_data:
        new_project = Project(**data.dict())
        db.add(new_project)
    try:
        await db.commit()
        new_project_id = new_project.project_id
        return {"message": "Project created successfully", "Project ID": new_project_id}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating project: {e}")


@app.put('/api/project/{project_id}/')
async def update_project(project_id: int, update_data: t.Project, db: AsyncSession = Depends(m.get_db_session)):
    Project = m.Base.classes.project

    try:
        update_successful = await h.universal_update(Project, db, project_id, update_data)
        if update_successful:
            return {"status": "success", "message": "Project updated successfully."}
        else:
            raise HTTPException(status_code=404, detail="Project not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating project: {e}")


@app.get("/api/project/employee/{project_id}/")
async def search_project_employee(project_id: int, db: AsyncSession = Depends(m.get_db_session)):
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
            Team.team_name
        )
        .join(ConnectionTeamEmployee, Employee.employee_id == ConnectionTeamEmployee.employee_id)
        .join(Team, ConnectionTeamEmployee.team_id == Team.team_id)
        .join(Project, Team.project_id == Project.project_id)
        .join(Exp_Level, Employee.experience_level_id == Exp_Level.experience_level_id)
        .join(Type, Employee.type_id == Type.type_id)
        .filter(Project.project_id == project_id)
    )
    db.expire_all()

    employees = [{
        'employee_id': row.employee_id,
        'first_name': row.first_name,
        'last_name': row.last_name,
        'free_fte': row.free_fte,
        'e_mail': row.e_mail,
        'phone_number': row.phone_number,
        'entry_date': row.entry_date,
        'exp_lvl_description': row.exp_lvl_description,
        'type_name': row.type_name,
        'team_name': row.team_name
    } for row in result.mappings().all()]

    return {"employee": employees}


@app.get("/api/project/team/{project_id}/")
async def search_project_team(project_id: int, db: AsyncSession = Depends(m.get_db_session)):
    Project = m.Base.classes.project
    Team = m.Base.classes.team

    result = await db.execute(
        select(
            Team.team_id,
            Team.team_name,
            Team.team_purpose
        )
        .join(Project, Team.project_id == Project.project_id)
        .filter(Project.project_id == project_id)
    )
    db.expire_all()

    teams = [{
        'team_id': row.team_id,
        'team_name': row.team_name,
        'team_purpose': row.team_purpose
    } for row in result.mappings().all()]

    return {"team": teams}


@app.post("/api/team/employee/")
async def assign_employee_to_team(team_data: List[t.ConnectionTeamEmployee],db: AsyncSession = Depends(m.get_db_session)):
    ConnectionTeamEmployee = m.Base.classes.connection_team_employee

    for data in team_data:
        new_connection = ConnectionTeamEmployee(**data.dict())
        db.add(new_connection)
    try:
        await db.commit()
        return {"message": "Employees assigned to team successfully"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Error assigning employees to team: {e}")


# CRUD operations for team table
@app.get('/api/team/')
async def get_team(db: AsyncSession = Depends(m.get_db_session)):
    Team = m.Base.classes.team
    Project = m.Base.classes.project

    result = await db.execute(
        select(
            Team.team_id,
            Team.team_name,
            Team.team_purpose,
            Project.proj_name
        )
        .join(Project, Team.project_id == Project.project_id)
    )
    db.expire_all()

    teams = [{
        'team_id': row.team_id,
        'team_name': row.team_name,
        'team_purpose': row.team_purpose,
        'project_name': row.proj_name
    } for row in result.mappings().all()]

    return {"team": teams}


@app.get('/api/team/{team_id}/')
async def get_team_by_id(team_id: int, db: AsyncSession = Depends(m.get_db_session)):
    Team = m.Base.classes.team
    Project = m.Base.classes.project

    result = await db.execute(
        select(
            Team.team_id,
            Team.team_name,
            Team.team_purpose,
            Project.proj_name
        )
        .join(Project, Team.project_id == Project.project_id)
        .where(Team.team_id == team_id)
    )
    db.expire_all()

    team = [{
        'team_id': row.team_id,
        'team_name': row.team_name,
        'team_purpose': row.team_purpose,
        'project_name': row.proj_name
    } for row in result.mappings().all()]

    return {"team": team}


@app.delete("/api/team/{team_id}/")
async def delete_team(team_id: int, db: AsyncSession = Depends(m.get_db_session)):
    Team = m.Base.classes.team
    ConnectionTeamEmployee = m.Base.classes.connection_team_employee
    try:
        deletion_successful = await h.universal_delete(Team, db, team_id=team_id)
        deletion_casc_connection = await h.universal_delete(ConnectionTeamEmployee, db, team_id=team_id)
        if deletion_successful and deletion_casc_connection:
            return {"status": "success", "message": "Team deleted successfully."}
        else:
            raise HTTPException(status_code=404, detail="Team not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting team: {e}")


@app.post('/api/team/')
async def create_team(team_data: List[t.Team], db: AsyncSession = Depends(m.get_db_session)):
    Team = m.Base.classes.team

    for data in team_data:
        new_team = Team(**data.dict())
        db.add(new_team)
    try:
        await db.commit()
        return {"message": "Team created successfully"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating team: {e}")


@app.put("/api/team/{team_id}/")
async def update_team(team_id: int, update_data: t.Team, db: AsyncSession = Depends(m.get_db_session)):
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
async def search_team_employee(team_id: int, db: AsyncSession = Depends(m.get_db_session)):
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
            Type.type_name
        )
        .join(ConnectionTeamEmployee, Employee.employee_id == ConnectionTeamEmployee.employee_id)
        .join(Team, ConnectionTeamEmployee.team_id == Team.team_id)
        .join(Exp_Level, Employee.experience_level_id == Exp_Level.experience_level_id)
        .join(Type, Employee.type_id == Type.type_id)
        .filter(Team.team_id == team_id)
    )
    db.expire_all()

    employees = [{
        'employee_id': row.employee_id,
        'first_name': row.first_name,
        'last_name': row.last_name,
        'free_fte': row.free_fte,
        'e_mail': row.e_mail,
        'phone_number': row.phone_number,
        'entry_date': row.entry_date,
        'exp_lvl_description': row.exp_lvl_description,
        'type_name': row.type_name
    } for row in result.mappings().all()]

    return {"employee": employees}


# Read definition tables (Team, Address, Type, Education Degree, Job, Skill, Experience Level)
@app.get('/api/department/')
async def get_department(db: AsyncSession = Depends(m.get_db_session)):
    Department = m.Base.classes.department
    result = await db.execute(
        select(Department)
    )
    departments = result.mappings().all()

    return {"department": departments}


@app.get('/api/address/')
async def get_address(db: AsyncSession = Depends(m.get_db_session)):
    Address = m.Base.classes.address
    result = await db.execute(
        select(Address)
    )
    addresses = result.mappings().all()

    return {"address": addresses}


@app.get('/api/type/')
async def get_type(db: AsyncSession = Depends(m.get_db_session)):
    Type = m.Base.classes.type
    result = await db.execute(
        select(Type)
    )
    types = result.mappings().all()

    return {"type": types}


@app.get('/api/education_degree/')
async def get_education_degree(db: AsyncSession = Depends(m.get_db_session)):
    Education_degree = m.Base.classes.education_degree
    result = await db.execute(
        select(Education_degree)
    )
    edu_degrees = result.mappings().all()

    return {"education_degree": edu_degrees}


@app.get('/api/job/')
async def get_job(db: AsyncSession = Depends(m.get_db_session)):
    Job = m.Base.classes.job
    result = await db.execute(
        select(Job)
    )
    jobs = result.mappings().all()

    return {"job": jobs}


@app.get('/api/skill/')
async def get_skill(db: AsyncSession = Depends(m.get_db_session)):
    Skill = m.Base.classes.skill
    result = await db.execute(
        select(Skill)
    )
    skills = result.mappings().all()

    return {"skill": skills}


@app.get('/api/experience_level/')
async def get_experience_level(db: AsyncSession = Depends(m.get_db_session)):
    Experience_level = m.Base.classes.experience_level
    result = await db.execute(
        select(Experience_level)
    )
    exp_levels = result.mappings().all()

    return {"experience_level": exp_levels}


# Login API
@app.post('/api/login/')
async def login(data: t.User_Login, db: AsyncSession = Depends(m_login.get_db_session_login)):
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


@app.post('/api/verifyToken')
async def verify_token(token: t.Token):
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
