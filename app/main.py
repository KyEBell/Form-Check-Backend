import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.database import create_db_and_tables, seed_system_tags
from app.routers import videos, tags, auth, users

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    seed_system_tags()
    yield


app = FastAPI(lifespan=lifespan)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again later."},
    )


app.include_router(auth.router)
app.include_router(videos.router)
app.include_router(tags.router)
app.include_router(users.router)


@app.get("/")
def root():
    return {"message": "Form Check Backend Running"}


@app.get("/health")
def health():
    return {"status": "ok"}
