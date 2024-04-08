from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from ORM.mapper import Mapper as mapper
from helper import Helper as helper
import ORM.tables as tables

mapper = mapper()
app = FastAPI()

# Event handlers

@app.on_event("startup")
async def startup_event():
    await mapper.reflect_tables()


@app.on_event("shutdown")
async def shutdown_event():
    await mapper.engine.dispose()

# API endpoints

# Search endpoint

@app.post("/search/")
async def search(criteria: tables.SearchCriteria, db: AsyncSession = Depends(mapper.get_db_session)):
    query = await helper.build_search_query(criteria.dict(exclude_none=True), db)
    result = await db.execute(query)
    await db.commit() 
    data = result.mappings().all()

    return {"data": data}

# CRUD operations for the Employee table

@app.get('/api/employee/')
async def get_personal(db: AsyncSession = Depends(mapper.get_db_session)):
    Employee = mapper.Base.classes.employee
    Exp_Level = mapper.Base.classes.experience_level
    Type = mapper.Base.classes.type

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

    return {"personal": employees}

@app.delete("/api/employee/{employee_id}/")
async def delete_employee(employee_id: int, db: AsyncSession = Depends(mapper.get_db_session)):
    Employee = mapper.Base.classes.employee
    try:
        deletion_successful = await helper.universal_delete(Employee, db, employee_id=employee_id)
        if deletion_successful:
            return {"status": "success", "message": "Employee deleted successfully."}
        else:
            raise HTTPException(status_code=404, detail="Employee not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting employee: {e}")


@app.post("/api/employee/")
async def create_employees(employee_data: List[tables.Employee], db: AsyncSession = Depends(mapper.get_db_session)):
    Employee = mapper.Base.classes.employee

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
async def update_employee(employee_id: int, update_data: tables.Employee, db: AsyncSession = Depends(mapper.get_db_session)):
    Employee = mapper.Base.classes.employee
    update_data_dict = update_data.dict(exclude_none=True)

    try:
        update_successful = await helper.universal_update(Employee, db, employee_id, update_data_dict)
        if update_successful:
            return {"status": "success", "message": "Employee updated successfully."}
        else:
            raise HTTPException(status_code=404, detail="Employee not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating employee: {e}")
    
# Read Internal, External, Stat employees

@app.get('/api/internal/')
async def get_internal(db: AsyncSession = Depends(mapper.get_db_session)):
    Employee = mapper.Base.classes.employee
    Exp_Level = mapper.Base.classes.experience_level
    Type = mapper.Base.classes.type

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
async def get_external(db: AsyncSession = Depends(mapper.get_db_session)):
    Employee = mapper.Base.classes.employee
    Exp_Level = mapper.Base.classes.experience_level
    Type = mapper.Base.classes.type

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
async def get_stat(db: AsyncSession = Depends(mapper.get_db_session)):
    Employee = mapper.Base.classes.employee
    Exp_Level = mapper.Base.classes.experience_level
    Type = mapper.Base.classes.type

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
async def get_project(db: AsyncSession = Depends(mapper.get_db_session)):
    Project = mapper.Base.classes.project
    Department = mapper.Base.classes.department
    Employee = mapper.Base.classes.employee

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

@app.delete("/api/project/{project_id}/")
async def delete_project(project_id: int, db: AsyncSession = Depends(mapper.get_db_session)):
    Project = mapper.Base.classes.project
    try:
        deletion_successful = await helper.universal_delete(Project, db, project_id=project_id)
        if deletion_successful:
            return {"status": "success", "message": "Project deleted successfully."}
        else:
            raise HTTPException(status_code=404, detail="Project not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting project: {e}")
    
@app.post("/api/project/")
async def create_project(project_data: List[tables.Project], db: AsyncSession = Depends(mapper.get_db_session)):
    Project = mapper.Base.classes.project

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
async def update_project(projecte_id: int, update_data: tables.Project, db: AsyncSession = Depends(mapper.get_db_session)):
    Project = mapper.Base.classes.employee
    update_data_dict = update_data.dict(exclude_none=True)

    try:
        update_successful = await helper.universal_update(Project, db, projecte_id, update_data_dict)
        if update_successful:
            return {"status": "success", "message": "Project updated successfully."}
        else:
            raise HTTPException(status_code=404, detail="Project not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating project: {e}")

# Read Team, Address, Type, Education Degree, Job, Skill, Experience Level

@app.get('/api/department/')
async def get_department(db: AsyncSession = Depends(mapper.get_db_session)):
    Department = mapper.Base.classes.department
    result = await db.execute(
        select(Department)
    )
    departments = result.mappings().all()

    return {"department": departments}


@app.get('/api/address/')
async def get_address(db: AsyncSession = Depends(mapper.get_db_session)):
    Address = mapper.Base.classes.address
    result = await db.execute(
        select(Address)
    )
    addresses = result.mappings().all()

    return {"address": addresses}


@app.get('/api/type/')
async def get_type(db: AsyncSession = Depends(mapper.get_db_session)):
    Type = mapper.Base.classes.type
    result = await db.execute(
        select(Type)
    )
    types = result.mappings().all()

    return {"type": types}


@app.get('/api/education_degree/')
async def get_education_degree(db: AsyncSession = Depends(mapper.get_db_session)):
    Education_degree = mapper.Base.classes.education_degree
    result = await db.execute(
        select(Education_degree)
    )
    edu_degrees = result.mappings().all()

    return {"education_degree": edu_degrees}


@app.get('/api/job/')
async def get_job(db: AsyncSession = Depends(mapper.get_db_session)):
    Job = mapper.Base.classes.job
    result = await db.execute(
        select(Job)
    )
    jobs = result.mappings().all()

    return {"job": jobs}


@app.get('/api/skill/')
async def get_skill(db: AsyncSession = Depends(mapper.get_db_session)):
    Skill = mapper.Base.classes.skill
    result = await db.execute(
        select(Skill)
    )
    skills = result.mappings().all()

    return {"skill": skills}


@app.get('/api/experience_level/')
async def get_experience_level(db: AsyncSession = Depends(mapper.get_db_session)):
    Experience_level = mapper.Base.classes.experience_level
    result = await db.execute(
        select(Experience_level)
    )
    exp_levels = result.mappings().all()

    return {"experience_level": exp_levels}