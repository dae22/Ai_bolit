from fastapi import FastAPI
from models.models import *
from databases import Database
from datetime import timedelta, date, time, datetime

app = FastAPI()

DATABASE_URL = "url"
database = Database(DATABASE_URL)

def get_daily_schedule(freq):
    start = timedelta(hours=8)
    interval = timedelta(hours=14/freq)
    daily_schedule = [time(hour=8)]
    freq -= 1
    for i in range(freq):
        start += interval
        minutes = start.seconds //60 % 60
        if minutes % 15 != 0:
            minutes = minutes // 15 * 15 + 15
        curr_time = time(hour=start.seconds // 3600, minute=minutes)
        daily_schedule.append(curr_time)
    return daily_schedule


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/schedule")
async def create_schedule(medicine: Medicine):
    med_start = date.today()
    med_end = med_start + timedelta(days=medicine.duration)
    query = ("""INSERT INTO schedules (medicine_name, frequency, duration, start, end, user_id)
             VALUES (:medicine_name, :frequency, :duration, :start, :end, :user_id) RETURNING id""")
    values = {"medicine_name": medicine.name, "frequency": medicine.frequency, "duration": medicine.duration,
              "start": med_start, "end": med_end, "user_id": medicine.user_id}
    schedule_id = await database.execute(query=query, values=values)
    return {"schedule_id": schedule_id}


@app.get("/schedules")
async def get_schedules(user_id: int):
    query = "SELECT id FROM schedules WHERE user_id=:user_id"
    values = {"user_id": user_id}
    rows = await database.fetch_all(query=query, values=values)
    schedules = [row["id"] for row in rows if row["end"] > date.today()]
    if not schedules:
        return {"message": "There are no actual schedules"}
    else:
        return {"schedule": schedules}


@app.get("/schedule")
async def get_schedule(user_id: int, schedule_id: int):
    query = "SELECT * FROM schedules WHERE user_id=:user_id AND id=:schedule_id"
    values = {"user_id": user_id, "schedule_id": schedule_id}
    row = await database.fetch_one(query=query, values=values)
    if row["end"] < date.today():
        return {"message": "Schedule outdated"}
    else:
        daily_schedule = get_daily_schedule(row["frequency"])
        return {"Daily schedule": daily_schedule}


@app.get("/next_taking")
async def take_next_pill(user_id: int):
    query = "SELECT * FROM scheduled WHERE user_id=:user_id"
    values = {"user_id": user_id}
    rows = await database.fetch_all(query=query, values=values)
    curr_time = time(hour=datetime.now().hour, minute=datetime.now().minute)
    end_time = time(hour=datetime.now().hour + 1, minute=datetime.now().minute)
    daily_schedules = []
    for row in rows:
        if row["end"] > date.today():
            row_schedule = get_daily_schedule(row["frequency"])
            for el in row_schedule:
                if curr_time < el < end_time:
                    daily_schedules.append([row["name"], el])
    daily_schedules.sort(key=lambda x: x[1])
    return {"Take pills within next hours": daily_schedules}
