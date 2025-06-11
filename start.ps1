# Activate the virtual environment
. .\.venv\Scripts\Activate.ps1

# Set the Ollama Host
$env:OLLAMA_HOST = "https://ollama.mydomain.com"

# Start the main Python script
python .\main.py