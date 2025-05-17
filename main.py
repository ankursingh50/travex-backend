from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from models import User
from routes.listings import router as listings_router  # ✅ Import router
import os

app = FastAPI()

app.include_router(listings_router)  # ✅ Register route

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/users")
async def get_users():
    return await User.all().values()

register_tortoise(
    app,
    db_url=os.getenv("DATABASE_URL").replace("postgresql://", "postgres://"),
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
