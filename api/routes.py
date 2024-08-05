from fastapi import FastAPI, File, UploadFile, HTTPException, APIRouter, Depends, Request
import os
from pathlib import Path
from database.session import db_dependency
from pdf_to_json import pdfreader
from .mistral import query
import json


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
    pdfreader(input,"output.txt")
    f = open("output.txt", "r")
    content = f.read()

    
    output1 = query({
        "inputs": """Functional Resume Sample """ + content + """ From this resume give a list of interview questions considering you are an interviewer. Only take into account the projects done. Give me 3 questions.""",
        "parameters": {
            "return_full_text": False
        }
    }) 

    output2 = query({
        "inputs": """Functional Resume Sample """ + content + """ From this resume give a list of interview questions considering you are an interviewer. Only take into account the work experience. Give me 3 questions.""",
        "parameters": {
            "return_full_text": False
        }
    })
    
    output3 = query({
        "inputs": """Functional Resume Sample """ + content + """ From this resume give a list of interview questions considering you are an interviewer. Give question from sections except projects and work experience. Give me 2 properly framed questions. This can include their clubs and chapters, publications, extracurricular activities or any other relevant fields""",
        "parameters": {
            "return_full_text": False
        }
    })

    output = []

    for qns in output1:
        out=(qns["generated_text"].split('\n'))
        for i in out:
            if len(i)>5:
                output.append(i[2::])
                
        
    for qns in output2:
        out=(qns["generated_text"].split('\n'))
        for i in out:
            if len(i)>5:
                output.append(i[2::])
        
    for qns in output3:
        out=(qns["generated_text"].split('\n'))
        for i in out:
            if len(i)>5:
                output.append(i[2::])
        
    return output





