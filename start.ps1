# Activate the virtual environment
. .\.venv\Scripts\Activate.ps1

#VBox NATed Env
$env:OLLAMA_HOST = "10.0.2.2"
$env:OLLAMA_BASE = "http://10.0.2.2:11434"

# Localhost Env
$env:OLLAMA_HOST = "127.0.0.1"
$env:OLLAMA_BASE = "http://127.0.0.1:11434"

# Start the main Python script
python .\main.py