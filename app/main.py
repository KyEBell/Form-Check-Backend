from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import create_db_and_tables
from app.routers import videos, tags, auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(videos.router)
app.include_router(tags.router)


@app.get("/")
def root():
    return {"message": "Form Check Backend Running"}


@app.get("/health")
def health():
    return {"status": "ok"}
