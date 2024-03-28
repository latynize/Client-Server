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
  "personal": [
    {
      "ID": 1,
      "Vorname": "Max",
      "Name": "Mustermann",
      "freie FTE": 0.5,
      "Mail": "max.mustermann@example.com",
      "Tel. Nummer": "123456789",
      "Beschäftigungsstart": "2023-01-01",
      "Erfahrungsgrad": "Fortgeschritten",
      "Typ": "Vollzeit"
    },
    {
      "ID": 2,
      "Vorname": "Lisa",
      "Name": "Müller",
      "freie FTE": 0.8,
      "Mail": "lisa.mueller@example.com",
      "Tel. Nummer": "987654321",
      "Beschäftigungsstart": "2022-05-15",
      "Erfahrungsgrad": "Anfänger",
      "Typ": "Teilzeit"
    },
    {
      "ID": 3,
      "Vorname": "Tom",
      "Name": "Schmidt",
      "freie FTE": 1.0,
      "Mail": "tom.schmidt@example.com",
      "Tel. Nummer": "456789123",
      "Beschäftigungsstart": "2021-09-30",
      "Erfahrungsgrad": "Erfahren",
      "Typ": "Vollzeit"
    }
  ]
}
"""
        # result = await database.fetch_all(query='SET search_path TO cioban;')
        result = json.loads(json_string)

        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Query execution error: {str(e)}")

