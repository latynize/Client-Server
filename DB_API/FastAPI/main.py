from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import mapper

mapper = mapper.Mapper()
app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await mapper.reflect_tables()


@app.on_event("shutdown")
async def shutdown_event():
    await mapper.engine.dispose()


@app.get('/api/personal/')
async def get_personal(db: AsyncSession = Depends(mapper.get_db)):
    Employee = mapper.Base.classes.employee
    Exp_Level = mapper.Base.classes.experience_level
    Type = mapper.Base.classes.type
    result = await db.execute(
        select(
            Employee,
            Exp_Level.exp_lvl_description,
            Type.type_name
        )
        .join(Exp_Level, Employee.experience_level_id == Exp_Level.experience_level_id)
        .join(Type, Employee.type_id == Type.type_id)
    )

    exclude_columns = ['experience_level_id', 'type_id', 'address_id']

    employees = [
        {
            **mapper.model_to_dict(employee, exclude_columns=exclude_columns),
            "exp_lvl_description": exp_lvl_description,
            "type_name": type_name
        }
        for employee, exp_lvl_description, type_name in result.all()
    ]
    return {"personal": employees}


@app.get('/api/internal/')
async def get_internal(db: AsyncSession = Depends(mapper.get_db)):
    Employee = mapper.Base.classes.employee
    Exp_Level = mapper.Base.classes.experience_level
    Type = mapper.Base.classes.type
    result = await db.execute(
        select(
            Employee,
            Exp_Level.exp_lvl_description,
            Type.type_name
        )
        .join(Exp_Level, Employee.experience_level_id == Exp_Level.experience_level_id)
        .join(Type, Employee.type_id == Type.type_id)
        .where(Employee.type_id == 1)
    )

    exclude_columns = ['experience_level_id', 'type_id', 'address_id']

    internals = [
        {
            **mapper.model_to_dict(internal, exclude_columns=exclude_columns),
            "exp_lvl_description": exp_lvl_description,
            "type_name": type_name
        }
        for internal, exp_lvl_description, type_name in result.all()
    ]
    return {"internal": internals}


@app.get('/api/external/')
async def get_external(db: AsyncSession = Depends(mapper.get_db)):
    Employee = mapper.Base.classes.employee
    Exp_Level = mapper.Base.classes.experience_level
    Type = mapper.Base.classes.type
    result = await db.execute(
        select(
            Employee,
            Exp_Level.exp_lvl_description,
            Type.type_name
        )
        .join(Exp_Level, Employee.experience_level_id == Exp_Level.experience_level_id)
        .join(Type, Employee.type_id == Type.type_id)
        .where(Employee.type_id == 2)
    )

    exclude_columns = ['experience_level_id', 'type_id', 'address_id']

    externals = [
        {
            **mapper.model_to_dict(external, exclude_columns=exclude_columns),
            "exp_lvl_description": exp_lvl_description,
            "type_name": type_name
        }
        for external, exp_lvl_description, type_name in result.all()
    ]
    return {"external": externals}


@app.get('/api/stat/')
async def get_stat(db: AsyncSession = Depends(mapper.get_db)):
    Employee = mapper.Base.classes.employee
    Exp_Level = mapper.Base.classes.experience_level
    Type = mapper.Base.classes.type
    result = await db.execute(
        select(
            Employee,
            Exp_Level.exp_lvl_description,
            Type.type_name
        )
        .join(Exp_Level, Employee.experience_level_id == Exp_Level.experience_level_id)
        .join(Type, Employee.type_id == Type.type_id)
        .where(Employee.type_id == 3)
    )

    exclude_columns = ['experience_level_id', 'type_id', 'address_id']

    stats = [
        {
            **mapper.model_to_dict(stat, exclude_columns=exclude_columns),
            "exp_lvl_description": exp_lvl_description,
            "type_name": type_name
        }
        for stat, exp_lvl_description, type_name in result.all()
    ]
    return {"stat": stats}


@app.get('/api/project/')
async def get_project(db: AsyncSession = Depends(mapper.get_db)):
    Project = mapper.Base.classes.project
    Department = mapper.Base.classes.department
    Employee = mapper.Base.classes.employee
    result = await db.execute(
        select(
            Project,
            Department.dep_name,
            Employee.last_name
        )
        .join(Department, Project.department_id == Department.department_id)
        .join(Employee, Project.proj_manager == Employee.employee_id)
    )

    exclude_columns = ['department_id', 'proj_manager']

    projects = [
        {
            **mapper.model_to_dict(project, exclude_columns=exclude_columns),
            "dep_name": dep_name,
            "last_name": last_name
        }
        for project, dep_name, last_name in result.all()
    ]
    return {"project": projects}


@app.get('/api/department/')
async def get_department(db: AsyncSession = Depends(mapper.get_db)):
    Department = mapper.Base.classes.department
    result = await db.execute(
        select(Department)
    )
    departments = result.scalars().all()
    return {"department": [mapper.model_to_dict(department) for department in departments]}


@app.get('/api/address/')
async def get_address(db: AsyncSession = Depends(mapper.get_db)):
    Address = mapper.Base.classes.address
    result = await db.execute(
        select(Address)
    )
    addresses = result.scalars().all()
    return {"address": [mapper.model_to_dict(address) for address in addresses]}


@app.get('/api/type/')
async def get_type(db: AsyncSession = Depends(mapper.get_db)):
    Type = mapper.Base.classes.type
    result = await db.execute(
        select(Type)
    )
    types = result.scalars().all()
    return {"type": [mapper.model_to_dict(type) for type in types]}


@app.get('/api/education_degree/')
async def get_education_degree(db: AsyncSession = Depends(mapper.get_db)):
    Education_degree = mapper.Base.classes.education_degree
    result = await db.execute(
        select(Education_degree)
    )
    education_degree = result.scalars().all()
    return {"education_degree": [mapper.model_to_dict(education_degree) for education_degree in education_degree]}


@app.get('/api/job/')
async def get_job(db: AsyncSession = Depends(mapper.get_db)):
    Job = mapper.Base.classes.job
    result = await db.execute(
        select(Job)
    )
    jobs = result.scalars().all()
    return {"job": [mapper.model_to_dict(job) for job in jobs]}


@app.get('/api/skill/')
async def get_skill(db: AsyncSession = Depends(mapper.get_db)):
    Skill = mapper.Base.classes.skill
    result = await db.execute(
        select(Skill)
    )
    skills = result.scalars().all()
    return {"skill": [mapper.model_to_dict(skill) for skill in skills]}


@app.get('/api/experience_level/')
async def get_experience_level(db: AsyncSession = Depends(mapper.get_db)):
    Experience_level = mapper.Base.classes.experience_level
    result = await db.execute(
        select(Experience_level)
    )
    experience_levels = result.scalars().all()
    return {"experience_level": [mapper.model_to_dict(experience_level) for experience_level in experience_levels]}
