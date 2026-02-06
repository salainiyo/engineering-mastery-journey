from typing import Optional
from sqlmodel import SQLModel, Field

class BaseHero(SQLModel):
    name: str = Field(index=True)
    age: int = Field(index=True)
    
class Hero(BaseHero, table=True):
    id: int = Field(default=None, primary_key=True)
    secret_name: str = Field()
    
class PublicHero(BaseHero):
    id: int
    
class CreateHero(BaseHero):
    secret_name : str
    
class UpdateHero(SQLModel):
    name: Optional[str] = None
    age: Optional[int] = None
    secret_name: Optional[str] = None