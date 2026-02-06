from sqlmodel import create_engine, SQLModel, Session
from fastapi import Depends
from typing import Annotated

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