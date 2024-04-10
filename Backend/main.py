from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import aliased
from sqlalchemy import or_
from sqlalchemy.sql import func
from typing import List, Optional
from ORM.mapper import Mapper
from helper import Helper as h
import ORM.tables as t

m = Mapper()
app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await m.reflect_tables()


@app.on_event("shutdown")
async def shutdown_event():
    await m.engine.dispose()

# API endpoints

# Search endpoint

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
                .join(ConnectionTeamEmployee, Employee.employee_id == ConnectionTeamEmployee.employee_id) \
                .join(Team, ConnectionTeamEmployee.team_id == Team.team_id) \
                .join(Project, Team.project_id == Project.project_id) \
                .join(Department, Project.department_id == Department.department_id) \
                .filter(Department.dep_name == criteria.department)

            if criteria.job is not None:
                Job_Internal = aliased(Job)
                Job_External = aliased(Job)
                query = query \
                    .join(Internal, Employee.employee_id == Internal.employee_id, isouter=True) \
                    .join(Job_Internal, Internal.job_id == Job_Internal.job_id, isouter=True) \
                    .join(External, Employee.employee_id == External.employee_id, isouter=True) \
                    .join(Job_External, External.job_id == Job_External.job_id, isouter=True) \
                    .filter(or_(
                        Job_Internal.job_name == criteria.job,
                        Job_External.job_name == criteria.job
                    ))
            if criteria.experienceLevel is not None:
                query = query \
                    .filter(ExperienceLevel.exp_lvl_description == criteria.experienceLevel)
            if criteria.project is not None:
                query = query \
                .join(ConnectionTeamEmployee, Employee.employee_id == ConnectionTeamEmployee.employee_id) \
                .join(Team, ConnectionTeamEmployee.team_id == Team.team_id) \
                .join(Project, Team.project_id == Project.project_id) \
                .filter(Project.proj_name == criteria.project)
            if criteria.type is not None:
                query = query \
                .join(Type, Employee.type_id == Type.type_id) \
                .filter(Type.type_name == criteria.type)
            if criteria.skill is not None:
                query = query \
                .join(Internal, Employee.employee_id == Internal.employee_id) \
                .join(Job, Internal.job_id == Job.job_id) \
                .join(External, Employee.employee_id == External.employee_id) \
                .join(Job, External.job_id == Job.job_id) \
                .join(ConnectionJobSkill, Job.job_id == ConnectionJobSkill.job_id) \
                .join(Skill, ConnectionJobSkill.skill_id == Skill.skill_id) \
                .filter(Skill.skill_name == criteria.skill)
            if criteria.fte is not None:
                query = query.filter(Employee.free_fte >= criteria.fte)

    result = await db.execute(query)

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
    

# search projects, read all employees in project

@app.get("/api/project/employee/{project_id}/")
async def search_project(project_id: int, db: AsyncSession = Depends(m.get_db_session)):
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


@app.delete("/api/employee/{employee_id}/")
async def delete_employee(employee_id: int, db: AsyncSession = Depends(m.get_db_session)):
    Employee = m.Base.classes.employee
    try:
        deletion_successful = await h.universal_delete(Employee, db, employee_id=employee_id)
        if deletion_successful:
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
    update_data_dict = update_data.dict(exclude_none=True)

    try:
        update_successful = await h.universal_update(Employee, db, employee_id, update_data_dict)
        if update_successful:
            return {"status": "success", "message": "Employee updated successfully."}
        else:
            raise HTTPException(status_code=404, detail="Employee not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating employee: {e}")


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
        .where (Employee.employee_id == employee_id)
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


@app.delete("/api/project/{project_id}/")
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


@app.post("/api/project/")
async def create_project(project_data: List[t.Project], db: AsyncSession = Depends(m.get_db_session)):
    Project = m.Base.classes.project

    for data in project_data:
        new_project = Project(**data.dict())
        db.add(new_project)
    try:
        await db.commit()
        return {"message": "Project created successfully"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating project: {e}")


@app.put("/api/project/{project_id}/")
async def update_project(project_id: int, update_data: t.Project, db: AsyncSession = Depends(m.get_db_session)):
    Project = m.Base.classes.employee
    update_data_dict = update_data.dict(exclude_none=True)

    try:
        update_successful = await h.universal_update(Project, db, project_id, update_data_dict)
        if update_successful:
            return {"status": "success", "message": "Project updated successfully."}
        else:
            raise HTTPException(status_code=404, detail="Project not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating project: {e}")

# Read Team, Address, Type, Education Degree, Job, Skill, Experience Level

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
