from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import text

# Assuming your models are correctly reflected or declared elsewhere
# from your_models import Employee

engine = create_async_engine("postgresql+asyncpg://postgres:post@localhost/postgres")
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = automap_base()

def model_to_dict(model_instance):
    for base in model_instance.__class__.__bases__:
        if hasattr(base, '__table__'):
            return {column.name: getattr(model_instance, column.name) for column in base.__table__.columns}
    return {}

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
    result = await db.execute(select(Employee))
    employees = result.scalars().all()
    return {"personal": [model_to_dict(employee) for employee in employees]}
