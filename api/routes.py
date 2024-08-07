from fastapi import FastAPI, File, UploadFile, HTTPException, APIRouter, Depends, Request
import os
from pathlib import Path
from database.session import db_dependency
from pdf_to_json import pdfreader
from .mistral import query
import json
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")


router = APIRouter()

UPLOAD_DIRECTORY = "uploaded_pdfs"

Path(UPLOAD_DIRECTORY).mkdir(parents=True, exist_ok=True)

@router.get("/pdf", response_class=HTMLResponse)
async def get_upload_form(request: Request):
    return templates.TemplateResponse("homepage.html", {"request": request})

@router.post("/upload-pdf/", response_class=HTMLResponse)
async def upload_pdf(request: Request, file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDFs are allowed.")
    
    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
    
    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to save file")
    
    pdfreader(file_path, "output.txt")
    
    
    return templates.TemplateResponse(
        "homepage.html", {"request": request}
    )


@router.get("/chatbot", response_class=HTMLResponse)
async def chatbot(request: Request):
    with open("output.txt", "r") as f:
        content = f.read()

    questions = []
    queries = [
        {
            "inputs": f"Functional Resume Sample {content} From this resume give a list of interview questions considering you are an interviewer. Only take into account the projects done. Give me 3 questions.",
            "parameters": {"return_full_text": False},
        },
        {
            "inputs": f"Functional Resume Sample {content} From this resume give a list of interview questions considering you are an interviewer. Only take into account the work experience. Give me 3 questions.",
            "parameters": {"return_full_text": False},
        },
        {
            "inputs": f"Functional Resume Sample {content} From this resume give a list of interview questions considering you are an interviewer. Give questions from sections except projects and work experience. Give me 2 properly framed questions. This can include their clubs and chapters, publications, extracurricular activities or any other relevant fields.",
            "parameters": {"return_full_text": False},
        },
    ]

    for query_data in queries:
        response = query(query_data)
        for qns in response:
            out = qns["generated_text"].split('\n')
            for i in out:
                if len(i) > 5:
                    questions.append(i[2:])
    print(questions)
    return templates.TemplateResponse("interview.html", {"request": request, "qns":questions})

