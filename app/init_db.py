import asyncpg
import asyncio

DATABASE_URL = "postgresql://dae22:1998@localhost/mydatabase"

async def create_table_schedules():
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute(''' CREATE TABLE IF NOT EXISTS schedules (
    id SERIAL PRIMARY KEY,
    medicine_name VARCHAR(255) NOT NULL,
    frequency INT NOT NULL,
    duration INT NOT NULL,
    start DATE NOT NULL,
    finish DATE NOT NULL,
    user_id INT NOT NULL 
    )
''')
    await conn.close()

asyncio.run(create_table_schedules())