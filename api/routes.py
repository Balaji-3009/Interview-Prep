from fastapi import FastAPI, File, UploadFile, HTTPException, APIRouter, Depends, Request
import os
from pathlib import Path
from database.session import db_dependency
from pdf_to_json import pdfreader
from .mistral import query


router = APIRouter()

UPLOAD_DIRECTORY = "uploaded_pdfs"

Path(UPLOAD_DIRECTORY).mkdir(parents=True, exist_ok=True)

@router.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDFs are allowed.")
    
    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
    
    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to save file")
    
    input = file_path
    pdfreader(input)
    f = open("output.txt", "r")
    content = f.read()

    output = query({
        "inputs": """Functional Resume Sample """ + content + """ From this resume give a list of interview questions considering you are an interviewer. Take into account the projects done and the work experience and ask questions from them.""",
        "parameters": {
            "return_full_text": False
        }
    })

    return output





