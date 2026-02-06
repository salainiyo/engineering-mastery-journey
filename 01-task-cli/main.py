from fastapi import FastAPI
from database import create_db
from routes import router

app = FastAPI()

@app.on_event("startup")
def on_strartup():
    create_db()
    
app.include_router(router)