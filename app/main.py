from fastapi import FastAPI
from app.models.models import *
from databases import Database

app = FastAPI()

DATABASE_URL = "url"
database = Database(DATABASE_URL)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/schedule")
async def create_schedule(medicine: Medicine):
    query = ("""INSERT INTO schedules (medicine_name, frequency, duration, user_id)
             VALUES (:medicine_name, :frequency, :duration, :user_id) RETURNING id""")
    values = medicine.dict()
    schedule_id = await database.execute(query=query, values=values)
    return {"schedule_id": schedule_id}



