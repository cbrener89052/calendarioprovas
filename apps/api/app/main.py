from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import text

from app.api.v1.router import api_router
from app.db.session import engine

app = FastAPI(
    title="calendarioprovas API",
    version="0.2.0",
    description="Plataforma multi-coordenador — calendário de provas",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/health")
def health() -> dict[str, str]:
    db_ok = "unknown"
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_ok = "ok"
    except Exception:
        db_ok = "error"
    return {"status": "ok", "service": "api", "database": db_ok}


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "calendarioprovas API — T4 upload + ingest grade"}
