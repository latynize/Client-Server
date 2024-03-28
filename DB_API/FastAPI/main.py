from fastapi import FastAPI, HTTPException
#from databases import Database
import sqlalchemy
import json

app = FastAPI()
# database = Database('postgresql://postgres:post@localhost/postgres')

@app.on_event("startup")
#async def startup():
    #await database.connect()

@app.on_event("shutdown")
#async def shutdown():
    #await database.disconnect()

@app.get('/api/personal/')
async def read_items():
    try:
        json_string = """
{
  "personen": [
    {"name": "Anna", "alter": 28, "beruf": "Ingenieurin"},
    {"name": "Bernd", "alter": 35, "beruf": "Lehrer"},
    {"name": "Carla", "alter": 24, "beruf": "Designerin"}
  ]
}
"""
        # result = await database.fetch_all(query='SET search_path TO cioban;')
        result = json.loads(json_string)

        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Query execution error: {str(e)}")

