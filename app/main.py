from fastapi import FastAPI
from models.models import *
from databases import Database

app = FastAPI()

DATABASE_URL = "url"
database = Database(DATABASE_URL)

def get_daily_schedule():
    pass

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

@app.get("/schedules")
async def get_schedules(user_id: int):
    query = "SELECT id FROM schedules WHERE user_id=:user_id"
    values = {"user_id": user_id}
    rows = await database.fetch_all(query=query, values=values)
    schedules = [row["id"] for row in rows]
    return {"schedule": schedules}

@app.get("/schedule")
async def get_schedule(user_id: int, schedule_id: int):
    query = "SELECT * FROM schedules WHERE user_id=:user_id AND id=:schedule_id"
    values = {"user_id": user_id, "schedule_id": schedule_id}
    row = await database.fetch_one(query=query, values=values)
    daily_schedule = get_daily_schedule()

@app.get("/next_taking")
async def take_next_pill(user_id: int)
    query = "SELECT * FROM scheduled WHERE user_id=:user_id"
    values = {"user_id": user_id}
    rows = await database.fetch_all(query=query, values=values)




