from sqlalchemy import create_engine, MetaData, select
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Session
import json
engine = create_engine("postgresql://postgres:post@localhost/postgres")

metadata = MetaData()

metadata.reflect(engine, schema="cioban", only=['employee', 'experience_level', 'type'])

Base = automap_base(metadata=metadata)

Base.prepare()

Employee = Base.classes.employee
Experience_level = Base.classes.experience_level
Type = Base.classes.type


# Constructing the query
query = select(
    Employee
)

def print_query(query, engine):
    session = Session(engine)
    result = session.execute(query).dict()
    employee = result.scalars().all()
    return {"personal": employee}   
