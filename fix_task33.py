import asyncio, asyncpg, os
from dotenv import load_dotenv

async def run_fix():
    load_dotenv(r'D:\SLH_CONTROL_PLANE\.env')
    url = os.getenv('DATABASE_URL').replace('+asyncpg', '')
    
    print(f"Connecting to DB...")
    conn = await asyncpg.connect(url)
    
    # עדכון ישיר של משימה 33
    query = "UPDATE agent_assignments SET agent_id = 36, status = 'in_progress' WHERE id = 33"
    result = await conn.execute(query)
    
    print(f"Update Result: {result}")
    
    # וידוא התוצאה
    new_status = await conn.fetchval("SELECT status FROM agent_assignments WHERE id = 33")
    print(f"New status in DB: {new_status}")
    
    await conn.close()

if __name__ == '__main__':
    asyncio.run(run_fix())
