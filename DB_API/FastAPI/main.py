from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import text

# Assuming your models are correctly reflected or declared elsewhere
# from your_models import Employee

engine = create_async_engine("postgresql+asyncpg://postgres:post@localhost/postgres", echo=True)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = automap_base()

def model_to_dict(model_instance, exclude_columns=None):
    exclude_columns = exclude_columns or []
    if hasattr(model_instance.__class__, '__table__'):
        table = model_instance.__class__.__table__
    return {
        column.name: getattr(model_instance, column.name)
        for column in table.columns
        if column.name not in exclude_columns
    }

async def reflect_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.prepare, reflect=True, schema="cioban")

app = FastAPI()

async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        await session.execute(text("SET search_path TO cioban"))
        yield session

@app.on_event("startup")
async def startup_event():
    await reflect_tables()  

@app.on_event("shutdown")
async def shutdown_event():
    await engine.dispose()

@app.get('/api/personal/')
async def get_personal(db: AsyncSession = Depends(get_db)):
    Employee = Base.classes.employee
    Exp_Level = Base.classes.experience_level
    Type = Base.classes.type
    result = await db.execute(
        select(
            Employee,
            Exp_Level.exp_lvl_description,
            Type.type_name
        )
        .join(Exp_Level, Employee.experience_level_id == Exp_Level.experience_level_id)
        .join(Type, Employee.type_id == Type.type_id)
    )
    
    # Specifying columns to exclude
    exclude_columns = ['experience_level_id', 'type_id', 'address_id']
    
    employees = [
        {
            **model_to_dict(employee, exclude_columns=exclude_columns),
            "exp_lvl_description": exp_lvl_description,
            "type_name": type_name
        }
        for employee, exp_lvl_description, type_name in result.all()
    ]
    
    return {"personal": employees}

@app.get('/api/internal/')
async def get_internal(db: AsyncSession = Depends(get_db)):
    Employee = Base.classes.employee
    Exp_Level = Base.classes.experience_level
    Type = Base.classes.type
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
    
    # Specifying columns to exclude
    exclude_columns = ['experience_level_id', 'type_id', 'address_id']
    
    internals = [
        {
            **model_to_dict(internal, exclude_columns=exclude_columns),
            "exp_lvl_description": exp_lvl_description,
            "type_name": type_name
        }
        for internal, exp_lvl_description, type_name in result.all()
    ]
    
    return {"internal": internals}

@app.get('/api/external/')
async def get_external(db: AsyncSession = Depends(get_db)):
    Employee = Base.classes.employee
    Exp_Level = Base.classes.experience_level
    Type = Base.classes.type
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
    
    # Specifying columns to exclude
    exclude_columns = ['experience_level_id', 'type_id', 'address_id']
    
    externals = [
        {
            **model_to_dict(external, exclude_columns=exclude_columns),
            "exp_lvl_description": exp_lvl_description,
            "type_name": type_name
        }
        for external, exp_lvl_description, type_name in result.all()
    ]
    
    return {"external": externals}

@app.get('/api/stat/')
async def get_stat(db: AsyncSession = Depends(get_db)):
    Employee = Base.classes.employee
    Exp_Level = Base.classes.experience_level
    Type = Base.classes.type
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
    
    # Specifying columns to exclude
    exclude_columns = ['experience_level_id', 'type_id', 'address_id']
    
    stats = [
        {
            **model_to_dict(stat, exclude_columns=exclude_columns),
            "exp_lvl_description": exp_lvl_description,
            "type_name": type_name
        }
        for stat, exp_lvl_description, type_name in result.all()
    ]
    
    return {"stat": stats}

@app.get('/api/project/')
async def get_project(db: AsyncSession = Depends(get_db)):
    Project = Base.classes.project
    Department = Base.classes.department
    Employee = Base.classes.employee
    result = await db.execute(
        select(
            Project,
            Department.dep_name,
            Employee.last_name
        )
        .join(Department, Project.department_id == Department.department_id)
        .join(Employee, Project.proj_manager == Employee.employee_id)
    )

        # Specifying columns to exclude
    exclude_columns = ['department_id', 'proj_manager']
    
    projects = [
        {
            **model_to_dict(project, exclude_columns=exclude_columns),
            "dep_name": dep_name,
            "last_name": last_name
        }
        for project, dep_name, last_name in result.all()
    ]
    
    return {"project": projects}

@app.get('/api/department/')
async def get_department(db: AsyncSession = Depends(get_db)):
    Department = Base.classes.department
    result = await db.execute(
        select(
            Department
        )
    )
    departments = result.scalars().all()
    return {"department": [model_to_dict(department) for department in departments]} 

@app.get('/api/address/')
async def get_address(db: AsyncSession = Depends(get_db)):
    Address = Base.classes.address
    result = await db.execute(
        select(
            Address
        )
    )
    addresses = result.scalars().all()
    return {"address": [model_to_dict(adress) for adress in addresses]} 
