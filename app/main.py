from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db

app = FastAPI()


@app.get('/')
async def health_check():
    return {'service': 'works'}


@app.get('/db_health')
async def db_health(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {'status': 'healthy', 'database': 'connected'}
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Database connection failed. Error:{e}"
        )
