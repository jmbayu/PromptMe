import os
import ollama

OLLAMA_HOST_URL = os.getenv("OLLAMA_HOST", "http://localhost:11434")
api_key = os.getenv("OLLAMA_API_KEY")

req_headers = {}
if api_key:
    req_headers["Authorization"] = f"Bearer {api_key}"

client = ollama.Client(host=OLLAMA_HOST_URL, headers=req_headers if req_headers else None)

def query_llm(prompt: str, model: str = 'granite3.1-moe:1b') -> str:
    try:
        res = client.generate(model=model, prompt=prompt)
        return res.get("response", "[No response]")
    except Exception as e:
        return f"[LLM Error]: {e}"
