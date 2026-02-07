from sqlmodel import SQLModel, Field
from typing import Optional

class BaseShoppingData(SQLModel):
    customer_gender: str = Field(nullable=False)
    customer_age: int = Field(nullable=False)
    season: str = Field(nullable=False)
    category: str = Field(nullable=False)
    product: str = Field(nullable=False)
    actual_price: float = Field(nullable=False)
    discount_applied: float = Field(nullable=False)
    customer_sentiment: str = Field(nullable=False)
    previous_sale: float =Field(nullable=False)
    
class ShoppingData(BaseShoppingData, table=True):
    id: int | None = Field(default=None, primary_key=True)