from fastapi import FastAPI
from app.database import create_db
from app.routes import router
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield create_db()
    
app = FastAPI(lifespan=lifespan)
app.include_router(router)