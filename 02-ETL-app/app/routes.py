from fastapi import APIRouter, Depends, Query
from .models import BaseShoppingData, ShoppingData
from .database import get_session
from sqlmodel import Session, select

router = APIRouter()

@router.get('/')
def home():
    return {
        "status":"active",
        "version":"1.0.0"
    } 
@router.get('/shopping/', response_model=list[ShoppingData])
def get_shopping_data(
                        offset: int = 0,
                        limit: int = Query(default=10, le=10),
                        session: Session = Depends(get_session)
                        ) -> list[ShoppingData]:
    shopping_data = session.exec(select(ShoppingData).offset(offset).limit(limit)).all()
    return list(shopping_data)