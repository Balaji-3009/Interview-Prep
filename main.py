from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from api.routes import router
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.include_router(router, prefix="/api", tags=["api"])

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {"message": "Hello World"} 
