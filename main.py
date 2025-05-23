from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise
from models import User
from routes.listings import router as listings_router
from routes.admin import router as admin_router
from routes.places import router as places_router
import os

app = FastAPI()

app.include_router(listings_router)
app.include_router(admin_router)
app.include_router(places_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/users")
async def get_users():
    return await User.all().values()

@app.get("/init-db")
async def init_db():
    await Tortoise.generate_schemas()
    return {"message": "Schema initialized."}

register_tortoise(
    app,
    db_url=os.getenv("DATABASE_URL").replace("postgresql://", "postgres://"),
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
