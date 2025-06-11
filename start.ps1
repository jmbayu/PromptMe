# Activate the virtual environment
. .\.venv\Scripts\Activate.ps1

# Set the Ollama Host
$env:OLLAMA_HOST = "https://ollama.mydomain.com"
$env:OLLAMA_API_KEY = "sk_xxxxx"

# Start the main Python script
python .\main.py