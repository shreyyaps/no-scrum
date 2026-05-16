from fastapi import FastAPI

from api.v1.router import api_router
from core.config import settings

app = FastAPI(title=settings.app_name)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
