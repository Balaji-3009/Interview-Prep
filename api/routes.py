from fastapi import FastAPI, File, UploadFile, HTTPException, APIRouter, Request
import io
import fitz  
from .mistral import query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .schema import getAnswers
import os
from pathlib import Path
import json
from .mistral_scoresheet import score

app = FastAPI()

templates = Jinja2Templates(directory="templates")

router = APIRouter()

pdf_content_storage = {}

@router.get("/pdf", response_class=HTMLResponse)
async def get_upload_form(request: Request):
    return templates.TemplateResponse("homepage.html", {"request": request})

@router.post("/upload-pdf/", response_class=HTMLResponse)
async def upload_pdf(request: Request, file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDFs are allowed.")
    
    try:
        pdf_content = await file.read()
        pdf_buffer = io.BytesIO(pdf_content)
        pdf_document = fitz.open(stream=pdf_buffer, filetype="pdf")
        
        pdf_output = ""
        for page in pdf_document:
            pdf_output += page.get_text()

        pdf_content_storage["pdf_output"] = pdf_output

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process the file: {str(e)}")
    
    return templates.TemplateResponse("homepage.html", {"request": request})

@router.get("/chatbot", response_class=HTMLResponse)
async def chatbot(request: Request):
    content = pdf_content_storage.get("pdf_output", None)
    
    if content is None:
        raise HTTPException(status_code=404, detail="No PDF content found. Please upload a PDF first.")
    
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
    return templates.TemplateResponse("interview.html", {"request": request, "qns": questions})

@router.post("/generate_result")
async def generate_result(ans: getAnswers):
    ip1 = ans.answers[:2]
    ip2 = ans.answers[2:4]
    ip3 = ans.answers[4:6]
    ip4 = ans.answers[6:]
    output = []
    op1 = score(ip1)
    output.append(op1)
    op2 = score(ip2)
    output.append(op2)
    op3 = score(ip3)
    output.append(op3)
    op4 = score(ip4)
    output.append(op4)
    return output
