from typing import Annotated, Optional
from sqlmodel import SQLModel, Field, create_engine, Session, select
from fastapi import FastAPI, Depends, Query, HTTPException

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
    
db_name = "database.db"
sqlite_url = f"sqlite:///{db_name}"
connect_args = {"check_same_thread":False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db():
    SQLModel.metadata.create_all(engine)
    
def get_session():
    with Session(engine) as session:
        yield session
        
SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI()

@app.on_event("startup")
def on_strartup():
    create_db()
    
@app.post('/heroes/', status_code=201, response_model=PublicHero)
def create_hero(hero: CreateHero, session:SessionDep):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

@app.get('/heroes/', response_model=list[PublicHero])
def get_heroes(session: SessionDep,
                offset: int = 0,
                limit: Annotated[int, Query(le=100)] = 100):
    heroes = session.exec(select(Hero).limit(limit).offset(offset)).all()
    return heroes

@app.get('/heroes/{id}', response_model=PublicHero)
def get_hero(session: SessionDep, id: int):
    hero = session.get(Hero, id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero

@app.delete('/heroes/{id}')
def delete_hero(session: SessionDep, id: int):
    hero = session.get(Hero, id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"Deleted":True}

@app.patch('/heroes/{id}', response_model=PublicHero)
def update_hero(id: int, session: SessionDep, hero: UpdateHero):
    hero_db = session.get(Hero, id)
    if not hero_db:
        raise HTTPException(status_code=404, detail="Hero not found")
    hero_data = hero.model_dump(exclude_unset=True)
    hero_db.sqlmodel_update(hero_data)
    session.add(hero_db)
    session.commit()
    session.refresh(hero_db)
    return hero_db
    