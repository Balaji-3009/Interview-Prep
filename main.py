from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from api.routes import router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from api.routes import get_upload_form

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.include_router(router, prefix="/api", tags=["api"])

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/",response_class = HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html",{"request": request}) 
