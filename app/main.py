from fastapi import FastAPI
from app.models.models import *
from databases import Database

app = FastAPI()

DATABASE_URL = "url"
database = Database(DATABASE_URL)

@app.on_event("startip")
async def startup():
    await database.connect()

@app.on_event("shotdown")
async def shutdown():
    await database.disconnect()

@app.post("/schedule",)
async def create_schedule(medicine: Medicine):
    pass