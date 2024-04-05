from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from ORM.mapper import Mapper
from helper import Helper

mapper = Mapper()
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "https://cioban.de",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    await mapper.reflect_tables()


@app.on_event("shutdown")
async def shutdown_event():
    await mapper.engine.dispose()


@app.get('/api/employee/')
async def get_personal(db: AsyncSession = Depends(mapper.get_db_session)):
    Employee = mapper.Base.classes.employee
    Exp_Level = mapper.Base.classes.experience_level
    Type = mapper.Base.classes.type

    result = await db.execute(
        select(Employee, Exp_Level.exp_lvl_description, Type.type_name)
        .join(Exp_Level, Employee.experience_level_id == Exp_Level.experience_level_id)
        .join(Type, Employee.type_id == Type.type_id)
    )

    order_columns = ['employee_id', 'first_name', 'last_name', 'free_fte', 'e_mail', 'phone_number', 'entry_date',
                     'exp_lvl_description', 'type_name']

    employees = []
    for row in result.all():
        employee, exp_lvl_description, type_name = row[0], row[1], row[2]
        employee_list = mapper.model_to_list(
            employee,
            order_columns=order_columns,
            additional_fields={'exp_lvl_description': exp_lvl_description, 'type_name': type_name}
        )
        employees.append(employee_list)

    return {"personal": employees}


@app.get('/api/internal/')
async def get_internal(db: AsyncSession = Depends(mapper.get_db_session)):
    Employee = mapper.Base.classes.employee
    Exp_Level = mapper.Base.classes.experience_level
    Type = mapper.Base.classes.type

    result = await db.execute(
        select(Employee, Exp_Level.exp_lvl_description, Type.type_name)
        .join(Exp_Level, Employee.experience_level_id == Exp_Level.experience_level_id)
        .join(Type, Employee.type_id == Type.type_id)
        .where(Employee.type_id == 1)
    )

    order_columns = ['employee_id', 'first_name', 'last_name', 'free_fte', 'e_mail', 'phone_number',
                     'exp_lvl_description', 'type_name']

    internals = []
    for row in result.all():
        employee, exp_lvl_description, type_name = row[0], row[1], row[2]
        internal_list = mapper.model_to_list(
            employee,
            order_columns=order_columns,
            additional_fields={'exp_lvl_description': exp_lvl_description, 'type_name': type_name}
        )
        internals.append(internal_list)

    return {"internal": internals}


@app.get('/api/external/')
async def get_external(db: AsyncSession = Depends(mapper.get_db_session)):
    Employee = mapper.Base.classes.employee
    Exp_Level = mapper.Base.classes.experience_level
    Type = mapper.Base.classes.type

    result = await db.execute(
        select(Employee, Exp_Level.exp_lvl_description, Type.type_name)
        .join(Exp_Level, Employee.experience_level_id == Exp_Level.experience_level_id)
        .join(Type, Employee.type_id == Type.type_id)
        .where(Employee.type_id == 2)
    )

    order_columns = ['employee_id', 'first_name', 'last_name', 'free_fte', 'e_mail', 'phone_number',
                     'exp_lvl_description', 'type_name']

    externals = []
    for row in result.all():
        employee, exp_lvl_description, type_name = row[0], row[1], row[2]
        external_list = mapper.model_to_list(
            employee,
            order_columns=order_columns,
            additional_fields={'exp_lvl_description': exp_lvl_description, 'type_name': type_name}
        )
        externals.append(external_list)

    return {"external": externals}


@app.get('/api/stat/')
async def get_stat(db: AsyncSession = Depends(mapper.get_db_session)):
    Employee = mapper.Base.classes.employee
    Exp_Level = mapper.Base.classes.experience_level
    Type = mapper.Base.classes.type

    result = await db.execute(
        select(Employee, Exp_Level.exp_lvl_description, Type.type_name)
        .join(Exp_Level, Employee.experience_level_id == Exp_Level.experience_level_id)
        .join(Type, Employee.type_id == Type.type_id)
        .where(Employee.type_id == 3)
    )

    order_columns = ['employee_id', 'first_name', 'last_name', 'free_fte', 'e_mail', 'phone_number',
                     'exp_lvl_description', 'type_name']

    stats = []
    for row in result.all():
        employee, exp_lvl_description, type_name = row[0], row[1], row[2]
        stat_list = mapper.model_to_list(
            employee,
            order_columns=order_columns,
            additional_fields={'exp_lvl_description': exp_lvl_description, 'type_name': type_name}
        )
        stats.append(stat_list)

    return {"stat": stats}


@app.get('/api/project/')
async def get_project(db: AsyncSession = Depends(mapper.get_db_session)):
    Project = mapper.Base.classes.project
    Department = mapper.Base.classes.department
    Employee = mapper.Base.classes.employee

    result = await db.execute(
        select(
            Project,
            Department.dep_name,
            Employee.last_name.label('supervisor')
        )
        .join(Department, Project.department_id == Department.department_id)
        .join(Employee, Project.proj_manager == Employee.employee_id)
    )

    order_columns = [
        'project_id', 'proj_name', 'dep_name', 'proj_priority',
        'supervisor', 'needed_fte', 'current_fte', 'start_date', 'end_date'
    ]

    exclude_columns = ['department_id', 'proj_manager']

    projects = []
    for row in result.all():
        project, dep_name, supervisor = row[0], row[1], row[2]

        project_list = mapper.model_to_list(
            project,
            exclude_columns,
            order_columns,
            additional_fields={'dep_name': dep_name, 'supervisor': supervisor}
        )

        projects.append(project_list)

    return {"project": projects}


@app.get('/api/department/')
async def get_department(db: AsyncSession = Depends(mapper.get_db_session)):
    Department = mapper.Base.classes.department
    result = await db.execute(
        select(Department)
    )
    departments = result.scalars().all()
    order_columns = ['department_id', 'dep_name', 'dep_description']
    department_list = [
        mapper.model_to_list(department, order_columns=order_columns)
        for department in departments
    ]
    return {"department": department_list}


@app.get('/api/address/')
async def get_address(db: AsyncSession = Depends(mapper.get_db_session)):
    Address = mapper.Base.classes.address
    result = await db.execute(
        select(Address)
    )
    addresses = result.scalars().all()
    order_columns = ['address_id', 'company', 'house_number', 'postcode', 'city', 'country']
    address_list = [
        mapper.model_to_list(address, order_columns=order_columns)
        for address in addresses
    ]
    return {"address": address_list}


@app.get('/api/type/')
async def get_type(db: AsyncSession = Depends(mapper.get_db_session)):
    Type = mapper.Base.classes.type
    result = await db.execute(
        select(Type)
    )
    types = result.scalars().all()
    order_columns = ['type_id', 'type_name', 'type_description']
    type_list = [
        mapper.model_to_list(type, order_columns=order_columns)
        for type in types
    ]
    return {"type": type_list}


@app.get('/api/education_degree/')
async def get_education_degree(db: AsyncSession = Depends(mapper.get_db_session)):
    Education_degree = mapper.Base.classes.education_degree
    result = await db.execute(
        select(Education_degree)
    )
    edu_degrees = result.scalars().all()
    order_columns = ['education_id', 'education_name']
    edu_degree_list = [
        mapper.model_to_list(edu_degree, order_columns=order_columns)
        for edu_degree in edu_degrees
    ]
    return {"education_degree": edu_degree_list}


@app.get('/api/job/')
async def get_job(db: AsyncSession = Depends(mapper.get_db_session)):
    Job = mapper.Base.classes.job
    result = await db.execute(
        select(Job)
    )
    jobs = result.scalars().all()
    order_columns = ['job_id', 'job_name', 'job_description', 'degree']
    job_list = [
        mapper.model_to_list(job, order_columns=order_columns)
        for job in jobs
    ]
    return {"job": job_list}


@app.get('/api/skill/')
async def get_skill(db: AsyncSession = Depends(mapper.get_db_session)):
    Skill = mapper.Base.classes.skill
    result = await db.execute(
        select(Skill)
    )
    skills = result.scalars().all()
    order_columns = ['skill_id', 'skill_name', 'skill_description']
    skill_list = [
        mapper.model_to_list(skill, order_columns=order_columns)
        for skill in skills
    ]
    return {"skill": skill_list}


@app.get('/api/experience_level/')
async def get_experience_level(db: AsyncSession = Depends(mapper.get_db_session)):
    Experience_level = mapper.Base.classes.experience_level
    result = await db.execute(
        select(Experience_level)
    )
    exp_levels = result.scalars().all()
    order_columns = ['experience_level_id', 'exp_lvl_description', 'years_of_experience']
    exp_level_list = [
        mapper.model_to_list(exp_level, order_columns=order_columns)
        for exp_level in exp_levels
    ]
    return {"experience_level": exp_level_list}


@app.delete("/api/employee/{employee_id}/")
async def delete_employee(employee_id: int, db: AsyncSession = Depends(mapper.get_db_session)):
    Employee = mapper.Base.classes.employee
    try:
        deletion_successful = await Helper.universal_delete(Employee, db, employee_id=employee_id)
        if deletion_successful:
            return {"status": "success", "message": "Employee deleted successfully."}
        else:
            raise HTTPException(status_code=404, detail="Employee not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting employee: {e}")


@app.post("/api/employee/")
async def create_employees(db: AsyncSession = Depends(mapper.get_db_session)):
    Employee = mapper.Base.classes.employee
    EmployeeCreate = Helper.create_pydantic_model_from_sqlalchemy(Employee, ['first_name', 'last_name', 'email',
                                                                             'position_id'])
    employee_data = List[EmployeeCreate]
    for data in employee_data:
        new_employee = Employee(**data.dict())
        db.add(new_employee)
    try:
        await db.commit()
        return {"message": "Employees created successfully"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating employee: {e}")
