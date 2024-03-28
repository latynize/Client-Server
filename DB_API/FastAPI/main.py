from fastapi import FastAPI, HTTPException
from databases import Database

app = FastAPI()
database = Database('postgresql://postgres:post@localhost/postgres')

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get('/api/personal/')
async def read_items():
    try:
        # Execute SQL query (BE VERY CAREFUL WITH RAW QUERIES!)
        result = await database.fetch_all(query='SET search_path TO cioban;')
        result = await database.fetch_all(query='SELECT em.employee_id, em.first_name, em.last_name, em.free_fte, em.e_mail, em.phone_number, em.entry_date, el.exp_lvl_description, t.type_name FROM employee em INNER JOIN experience_level el ON em.experience_level_id = el.experience_level_id INNER JOIN type t ON em.type_id = t.type_id;')
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Query execution error: {str(e)}")

