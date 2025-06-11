import os
import ollama

OLLAMA_HOST_URL = os.getenv("OLLAMA_HOST", "http://localhost:11434")

def query_llm(prompt: str, model: str = 'granite3.1-moe:1b') -> str:
    try:
        res = ollama.generate(model=model, prompt=prompt, options={"base_url": OLLAMA_HOST_URL})
        return res.get("response", "[No response]")
    except Exception as e:
        return f"[LLM Error]: {e}"
