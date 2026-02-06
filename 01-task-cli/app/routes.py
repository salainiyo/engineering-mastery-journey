from app.models import PublicHero, CreateHero, Hero, UpdateHero
from app.database import SessionDep
from sqlmodel import select
from fastapi import Query, HTTPException, APIRouter
from typing import Annotated

router = APIRouter()

@router.post('/heroes/', status_code=201, response_model=PublicHero)
def create_hero(hero: CreateHero, session:SessionDep):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

@router.get('/heroes/', response_model=list[PublicHero])
def get_heroes(session: SessionDep,
                offset: int = 0,
                limit: Annotated[int, Query(le=100)] = 100):
    heroes = session.exec(select(Hero).limit(limit).offset(offset)).all()
    return heroes

@router.get('/heroes/{id}', response_model=PublicHero)
def get_hero(session: SessionDep, id: int):
    hero = session.get(Hero, id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero

@router.delete('/heroes/{id}')
def delete_hero(session: SessionDep, id: int):
    hero = session.get(Hero, id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"Deleted":True}

@router.patch('/heroes/{id}', response_model=PublicHero)
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