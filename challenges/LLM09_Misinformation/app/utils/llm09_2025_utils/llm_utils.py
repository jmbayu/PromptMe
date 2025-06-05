import ollama
import os

OLLAMA_BASE = os.getenv("OLLAMA_BASE", "http://localhost:11434")

def query_llm(prompt):
    response = ollama.chat(model='mistral', messages=[{'role': 'user', 'content': prompt}], options={"base_url": OLLAMA_BASE})
    return response['message']['content']
