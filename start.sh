#!/bin/bash

# Activate the virtual environment
source .venv/bin/activate

# Set the environment variable
export OLLAMA_HOST="127.0.0.1"
export OLLAMA_HOST="10.0.2.2"


export OLLAMA_BASE="http://127.0.0.1:11434"
export OLLAMA_BASE="http://10.0.2.2:11434"



# Start the main Python script
python ./main.py