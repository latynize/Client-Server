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
    exclude_columns = []
    
    projects = [
        {
            **model_to_dict(project, exclude_columns=exclude_columns),
            "dep_name": dep_name,
            "type_name": last_name
        }
        for project, dep_name, last_name in result.all()
    ]
    
    return {"project": projects}
