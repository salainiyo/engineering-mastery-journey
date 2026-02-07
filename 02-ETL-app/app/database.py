from sqlmodel import create_engine, Session, SQLModel
from fastapi import Depends

sqlfile = "shopping.db"
sqlite_url = f"sqlite:///{sqlfile}"
engine = create_engine(
    sqlite_url,
    connect_args = {"check_same_thread":False}
)
def get_session():
    with Session(engine) as session:
        return session
    
def create_db():
    SQLModel.metadata.create_all(engine)