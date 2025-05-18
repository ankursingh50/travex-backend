from fastapi import APIRouter, HTTPException
from tortoise import Tortoise
import os

router = APIRouter()

@router.get("/reset-booking-table")
async def reset_booking_table():
    try:
        await Tortoise.init(
            db_url=os.getenv("DATABASE_URL").replace("postgresql://", "postgres://"),
            modules={"models": ["models"]},
        )
        await Tortoise.get_connection("default").execute_query("DROP TABLE IF EXISTS booking_listings CASCADE;")
        return {"message": "booking_listings table dropped. Now visit /init-db to recreate."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
