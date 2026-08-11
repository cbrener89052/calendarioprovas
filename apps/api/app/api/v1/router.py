from fastapi import APIRouter

from app.api.v1 import ingest, upload

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(upload.router)
api_router.include_router(ingest.router)
