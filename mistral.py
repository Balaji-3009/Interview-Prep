import requests
from pdf_to_json import pdfreader
from dotenv import load_dotenv
import os

input = "path_to_pdf"

pdfreader(input)
load_dotenv('.env')

f = open("output.txt", "r")
content = f.read()
hugging_face_api_key = os.getenv("HUGGING_FACE_API_KEY")

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
headers = {"Authorization": f"Bearer {hugging_face_api_key}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()
    
output = query({
    "inputs": """Functional Resume Sample """ + content + """ From this resume give a list of interview questions considering you are an interviewer. Take into account the projects done and the work experience and ask questions from them.""",
    "parameters": {
        "return_full_text": False
    }
})

print(output)