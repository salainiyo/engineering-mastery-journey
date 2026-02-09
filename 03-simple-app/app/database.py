from sqlmodel import Session, create_engine

sqlite_url = "sqlite:///cooperative.db"
engine = create_engine(sqlite_url, connect_args={"check_same_thread":False})

def get_session():
    with Session(engine) as session:
        return session
