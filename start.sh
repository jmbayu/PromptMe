#!/bin/bash

# Activate the virtual environment
source .venv/bin/activate

# Set the environment variable
export OLLAMA_HOST="https://ollama.mydomain.com"
export OLLAMA_API_KEY="sk_xxxxx"

# Start the main Python script
python ./main.py