import ollama
import os

def query_llm(prompt):
    ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    api_key = os.getenv("OLLAMA_API_KEY")

    req_headers = {}
    if api_key:
        req_headers["Authorization"] = f"Bearer {api_key}"

    client = ollama.Client(host=ollama_host, headers=req_headers if req_headers else None)
    response = client.chat(model='mistral', messages=[{'role': 'user', 'content': prompt}])
    return response['message']['content']
