from sqlalchemy import text
from src.services.db import engine

async def log_usage(user_id:int,event:str):

    if not engine:
        return

    async with engine.begin() as conn:
        await conn.execute(
            text(
                '''
                INSERT INTO usage_logs
                (user_id,event_name)
                VALUES
                (:u,:e)
                '''
            ),
            {
                "u":user_id,
                "e":event
            }
        )
