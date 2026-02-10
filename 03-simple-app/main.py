from fastapi import FastAPI
from app.routes.loan import loan_router
from app.routes.member import member_router
from app.routes.payment import payment_router
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    
app = FastAPI(lifespan=lifespan)
app.include_router(member_router)
app.include_router(loan_router)
app.include_router(payment_router)