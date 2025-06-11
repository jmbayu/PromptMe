import requests
import os
OLLAMA_URL = os.getenv("OLLAMA_HOST", "http://localhost:11434")
api_key = os.getenv("OLLAMA_API_KEY")

def generate_with_ollama(model_name, history, prompt):
    # Send the chat to Ollama's API
    req_headers = {}
    if api_key:
        req_headers["Authorization"] = f"Bearer {api_key}"

    response = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json={
            "model": model_name,
            "messages": history + [{"role": "user", "content": prompt}],
            "stream": False
            
        },
        headers=req_headers
    )
    response.raise_for_status()
    result = response.json()
    return result["message"]["content"]
