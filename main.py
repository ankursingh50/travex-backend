from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from models import User
from routes.listings import router as listings_router
from tortoise import Tortoise  # ✅ Import for schema generation
import os

app = FastAPI()

# ✅ Register route
app.include_router(listings_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/users")
async def get_users():
    return await User.all().values()

# ✅ Temporary route to regenerate schema
@app.get("/init-db")
async def init_db():
    await Tortoise.generate_schemas()
    return {"message": "Schema initialized."}

# ✅ Tortoise ORM setup
register_tortoise(
    app,
    db_url=os.getenv("DATABASE_URL").replace("postgresql://", "postgres://"),
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
