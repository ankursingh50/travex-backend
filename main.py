from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
import os

from models import User  # ✅ must be imported BEFORE register_tortoise

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/users")
async def get_users():
    return await User.all().values()

# ✅ Register after model is imported
register_tortoise(
    app,
    db_url=os.getenv("DATABASE_URL").replace("postgresql://", "postgres://"),
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
