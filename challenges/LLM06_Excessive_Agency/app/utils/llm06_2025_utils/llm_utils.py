import ollama
import os

def query_llm(prompt):
    base_url=os.getenv("OLLAMA_HOST", "http://localhost:11434")

    response = ollama.chat(model='mistral', options={"base_url": base_url},  messages=[{'role': 'user', 'content': prompt}])
    return response['message']['content']
