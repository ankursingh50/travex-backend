from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
import os

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Register Tortoise
register_tortoise(
    app,
    db_url=os.getenv("DATABASE_URL"),
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
