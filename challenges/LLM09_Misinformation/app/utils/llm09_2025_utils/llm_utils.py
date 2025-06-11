import ollama
import os

OLLAMA_HOST_URL = os.getenv("OLLAMA_HOST", "http://localhost:11434")
api_key = os.getenv("OLLAMA_API_KEY")

req_headers = {}
if api_key:
    req_headers["Authorization"] = f"Bearer {api_key}"

client = ollama.Client(host=OLLAMA_HOST_URL, headers=req_headers if req_headers else None)

def query_llm(prompt):
    response = client.chat(model='mistral', messages=[{'role': 'user', 'content': prompt}])
    return response['message']['content']
