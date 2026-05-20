import os
from pathlib import Path
from dotenv import load_dotenv

_env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(_env_path, override=True)

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routes import scrape, jobs, outlines

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not os.getenv("PALANTIR_SECRET"):
        raise RuntimeError("PALANTIR_SECRET env var is required but not set")
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="Palantir", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5180", "http://127.0.0.1:5180",
        "http://localhost:3000", "http://127.0.0.1:3000",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(scrape.router, prefix="/api", tags=["scrape"])
app.include_router(jobs.router, prefix="/api", tags=["jobs"])
app.include_router(outlines.router, prefix="/api", tags=["outlines"])

@app.get("/health")
def health():
    return {"status": "ok", "version": "1.0.0"}
