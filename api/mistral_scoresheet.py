import requests
from dotenv import load_dotenv
import os

load_dotenv('.env')
hugging_face_api_key = os.getenv("HUGGING_FACE_API_KEY")


API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
headers = {"Authorization": f"Bearer {hugging_face_api_key}"}


def score(input):
    qa_string = ""
    for qa in input:
        question = qa["question"]
        answer = qa["answer"]
        qa_string += f"Q: {question}\nA: {answer}\n\n"

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
        
    output = query({
        "inputs": qa_string + "Give an overall review for the answers in this string and suggest some improvements",
        "parameters": {
            "return_full_text": False
        }
    })
    return output