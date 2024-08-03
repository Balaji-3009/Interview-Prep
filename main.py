from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import database.models
from database.session import db_dependency, get_db
from database.session import engine
from sqlalchemy.orm import Session
from api.routes import router

app = FastAPI()

database.models.Base.metadata.create_all(bind = engine)

app.include_router(router, prefix="/api", tags=["api"])

@app.get("/")
async def root():
    return {"message": "Hello World"} 
