import ollama
import os

OLLAMA_HOST_URL = os.getenv("OLLAMA_HOST", "http://localhost:11434")

def query_llm(prompt):
    response = ollama.chat(model='mistral', messages=[{'role': 'user', 'content': prompt}], options={"base_url": OLLAMA_HOST_URL})
    return response['message']['content']
