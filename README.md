# PromptMe 


<p>
<img src="./static/logo.png?raw=true" width="600" alt="Thumbnail"/>
</p>

### A vulnerable application designed to demonstrate the OWASP Top 10 for Large Language Model (LLM) Applications 2025 .

* Educational project that showcases security vulnerabilities in large language models (LLMs) and their web integrations. 
* Includes 10 hands-on challenges inspired by the OWASP LLM Top 10, demonstrating how these vulnerabilities can be discovered and exploited in real-world scenarios.

This project is intended for AI Security professionals to explore potential security risks in LLMs and learn effective mitigation strategies.

# Top 10 2025

| Vulnerability | Short Description |
|-----------|-------------|
| LLM01: Prompt Injection | xxx |
| LLM02: Sensitive Information Disclosure | xxx |
| LLM03: Supply Chain | xxx |
| LLM04: Data and Model Poisoning | xxx |
| LLM05: Improper Output Handling | xxx |
| LLM06: Excessive Agency | xxx |
| LLM07: System Prompt Leakage | xxx |
| LLM08: Vector and Embedding Weaknesses | xxx |
| LLM09: Misinformation | xxx |
| LLM10: Unbounded Consumption | xxx |

# Demo: LLM01, LLM02, LLM06?, LLM07?
## Overview (No API Key required)

* The project is primarily developed using Python and the Ollama framework, with the open source LLM models. 
* The exercises are structured in the form of **CTF (Capture The Flag) challenges**, each with a clear objective, optional hints, and a flag awarded upon successful completion.

## Gettting started

This guide provides instructions for setting up and running the challenges.

### Prerequisites

* Python 3.10 or higher
* pip (Python package installer)
* ollama framework 

### Setup

#### 1. Install the dependencies.
> ```
> pip install -r requirements.txt
> ```

#### 2. Download and Run Ollama

> Download Ollama depending on your OS from https://ollama.com/download
>```
> ollama serve (in the separate terminal)
> ollama pull mistral
> ollama pull llama3.2:1b
> ollama pull sqlcoder
> ollama pull granite3.1-moe:1b
>```
>or Spawn Ollama via docker using the below command
> ```
> docker run -d --name ollama_server -p 11434:11434 ollama/ollama:latest
> docker exec -it ollama_server ollama pull <model_name>
> docker exec -it ollama_server ollama run <model_name>
> ```

#### 5. Access the application

> ```
> python main.py
> ```
Access the application @ http://127.0.0.1:5000

#### 6. Start the challenge by clicking *start* button on particular category e.g. LLM01


## Spoilers

[Solutions](https://github.com/R3dShad0w7/PromptMe/tree/main/solutions) to the challenges are provided for beginners who may not be familiar with exploiting vulnerabilities from the LLM Top 10. This guide is intended to help users solve the challenges and understand the underlying vulnerable code and components.


## Disclaimer

PromptMe is an intentionally vulnerable application created for educational purposes. Since the application uses insecure code and packages to demonstrate possible risks, it is strongly recommended to run it in a virtual or sandboxed environment.
Warning: The vulnerabilities shown in this project are for learning only and should never be implemented in production systems.

🤝 Contributing

We welcome contributions from the community! Whether you're fixing bugs, improving documentation, or suggesting new challenges, your help is appreciated.

# Original Source:
[https://github.com/R3dshad0w7/promptme](https://github.com/R3dshad0w7/promptme)
