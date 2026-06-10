from fastapi import FastAPI

from api.router import api_router
from core.config import settings

app = FastAPI(title=settings.app_name)

app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
def read_root():
    return {"Hello": "World"}
