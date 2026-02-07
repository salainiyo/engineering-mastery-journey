from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from app.database import create_db
from app.routes import router
from sqlmodel import Session, select
import pandas as pd
from pathlib import Path
from app.services import data_preprocessor
from app.database import engine
from app.models import BaseShoppingData, ShoppingData

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    with Session(engine) as session:
    
        file_path = Path('app/data/synthetic_shopping_data.csv')
        data = pd.read_csv(file_path)
        final_data = data_preprocessor(data)
        for _, row in final_data.iterrows():
            shopping_data = ShoppingData(
                customer_gender = row['customer_gender'],
                customer_age = row['customer_age'],
                season = row['season'],
                category= row['category'],
                product= row['product'],
                actual_price = row['actual_price'],
                discount_applied = row['discount_applied'],
                customer_sentiment = row['customer_sentiments'],
                previous_sale = row['previous_sales']
                )
            already_loaded = session.exec(select(ShoppingData)).first()
            if not already_loaded:
                session.add(shopping_data)
        session.commit()
        yield
    
app=FastAPI(lifespan=lifespan)
app.include_router(router)