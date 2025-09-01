import ollama
import os

client = ollama.Client(host=os.environ.get("OLLAMA_HOST", "http://localhost:11434"))

def query_llm(prompt):
    response = client.chat(model='mistral', messages=[{'role': 'user', 'content': prompt}])
    return response['message']['content']
