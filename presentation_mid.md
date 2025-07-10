# PromptMe: OWASP Top 10 for LLM Applications

This presentation provides an overview of the OWASP Top 10 vulnerabilities for Large Language Model (LLM) applications, as demonstrated by the "PromptMe" educational project. Each section details a vulnerability, its description, the vulnerable code segment within the demo application, mitigation strategies, and a link to the respective challenge.

Access the main dashboard for all challenges: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## LLM01: Prompt Injection

**Description:**
Prompt Injection occurs when user-supplied input alters the LLM’s behavior or output in unintended ways. These inputs can affect the model even if they are imperceptible to humans. The demo application allows users to interact with a chatbot, and the admin has stored a secret key in their chat history. The challenge is to use prompt injection to retrieve this secret key.

**Challenge Implementation Note:**
The application's `/fetch` command allows summarizing web content. This function incorporates the entire chat history (including admin's secret key) into the LLM prompt, making it vulnerable if a malicious URL's content instructs the LLM to reveal parts of that history.

**Mitigation:**
- Implement strict input sanitization and output encoding.
- Use distinct models or privilege separation for processing user-supplied content versus executing privileged actions.
- Avoid incorporating untrusted content directly into privileged prompts.
- Do not pass sensitive data (like other users' chat history or secret keys) into contexts where user input can influence the LLM's instructions.
- Ensure guardian models or safety checks are applied consistently, even for special commands like `/fetch`.

**Demo Link:** Access the LLM01 challenge via the main dashboard and navigate to its specific port (typically http://127.0.0.1:5001).

---

## LLM02: Sensitive Information Disclosure

**Description:**
This vulnerability occurs when an LLM inadvertently reveals sensitive data. In this challenge, a RAG (Retrieval-Augmented Generation) system is misconfigured, allowing it to expose a secret key from PDF documents when prompted appropriately.

**Challenge Implementation Note:**
The RAG system retrieves context from PDF files, one of which (`configuration.pdf`) contains a secret token. The LLM, despite a system prompt to not reveal secrets, can be prompted to disclose this token if it's part of the retrieved context.

**Mitigation:**
- Carefully curate and sanitize data sources used for RAG.
- Implement robust access controls on sensitive documents.
- Use techniques like data masking or redaction for sensitive information before it's fed into the LLM or vector store.
- Employ strong prompt engineering to prevent the LLM from divulging information outside its intended scope.
- Regularly audit knowledge bases for sensitive data.

**Demo Link:** Access the LLM02 challenge via the main dashboard (typically http://127.0.0.1:5002).

---
## LLM03: Supply Chain Risk

**Description:**
Supply chain vulnerabilities in LLMs can arise from compromised pre-trained models, poisoned training data, or insecure plugin integrations. This challenge demonstrates a rogue model that silently exfiltrates user chat data to an attacker's server.

**Challenge Implementation Note:**
A 'rogue_handler.py' for one of the selectable models includes a function `send_to_attacker_server` that exfiltrates chat history to a predefined local URL (`http://127.0.0.1:5012/exfil`) every time the rogue model generates a response.

**Mitigation:**
- Only use LLMs and components from trusted and verified sources.
- Implement checksums/hashes (e.g., SHA-256) for model files and verify them during deployment.
- Scan models for malicious code or unexpected behaviors.
- Limit model access to system-level APIs, environment variables, and network connections.
- Monitor outbound traffic from LLM applications.

**Demo Link:** Access the LLM03 challenge via the main dashboard (typically http://127.0.0.1:5003).

---

## LLM04: Data and Model Poisoning

**Description:**
Data poisoning occurs when pre-training, fine-tuning, or embedding data is manipulated to introduce vulnerabilities, backdoors, or biases. This challenge involves an LLM that answers questions based on a document (`owasp_llm_qa.csv`) which is made to be "publicly accessible and editable" (simulated by being in `test_docs/`). An attacker can modify this document to influence the chatbot's responses.

**Challenge Implementation Note:**
The application uses a CSV file (`test_docs/owasp_llm_qa.csv`) as its knowledge base for a Q&A bot. This file's location is revealed by asking the bot its source, and the challenge implies this file path is editable by an attacker to poison the RAG data.

**Mitigation:**
- Secure the data pipeline: protect training data, fine-tuning data, and RAG data sources from unauthorized modification.
- Implement version control and integrity checks for datasets.
- Do not rely on public or user-editable sources for trusted RAG input without strict validation and sandboxing.
- Continuously monitor document updates and log changes if using dynamic sources.
- Regularly audit models for unexpected behavior or biases.

**Demo Link:** Access the LLM04 challenge via the main dashboard (typically http://127.0.0.1:5004).

---

## LLM05: Improper Output Handling

**Description:**
This occurs when an LLM generates outputs that are not properly validated or constrained, potentially leading to vulnerabilities like SQL injection if the output is used to construct database queries. In this e-commerce application, the chatbot interacts with a SQLite3 database. The goal is to manipulate the chatbot's output to increase account credit.

**Challenge Implementation Note:**
The AI assistant in the e-commerce app (`Market/utils/llm_utils.py`) uses the `sqlcoder` model to convert natural language to SQL queries. These LLM-generated SQL queries are executed directly, allowing an attacker to prompt for malicious SQL (e.g., `UPDATE user SET budget = ...`) to alter their account balance.

**Mitigation:**
- Treat model outputs as untrusted user input. Apply robust input validation and sanitization before using LLM output in downstream systems (e.g., database queries, API calls).
- Use parameterized queries or ORMs instead of constructing SQL queries from LLM output directly.
- Implement strict allowlists for SQL commands or patterns if direct SQL generation is unavoidable. For example, only allow `SELECT` statements.
- Principle of least privilege for database users accessed by the LLM application.

**Demo Link:** Access the LLM05 challenge via the main dashboard (typically http://127.0.0.1:5005).

---

## LLM06: Excessive Agency

**Description:**
Excessive Agency occurs when LLMs are granted more permissions or capabilities than necessary, leading to unintended actions. This challenge involves a file management system where a flaw allows users to perform unauthorized actions by manipulating prompts.

**Challenge Implementation Note:**
The file management service (`app/utils/llm06_2025_utils/llm06_2025_service.py`) uses an LLM to parse user intent into a JSON action, including a 'role'. If a user claims to be an admin in the prompt, the LLM might set the role to 'BOX-ADMIN-OWNER', bypassing folder access restrictions.

**Mitigation:**
- Do not let the LLM determine user roles or permissions. User authentication and authorization should be handled by a separate, secure component based on established identity.
- Apply the principle of least privilege: LLMs should only have the minimum necessary permissions to perform their intended tasks.
- Implement strict input validation and action confirmation for any actions initiated by the LLM.
- Human oversight for critical actions.

**Demo Link:** Access the LLM06 challenge via the main dashboard (typically http://127.0.0.1:5006).

---

## LLM07: System Prompt Leakage

**Description:**
System Prompt Leakage occurs when sensitive information (e.g., API keys, instructions) embedded within the system prompt is extracted by an attacker through clever prompting. This challenge has an API key hidden in the system prompt.

**Challenge Implementation Note:**
The application embeds an `API_KEY` directly within the `system_prompt` given to the LLM. Although instructed not to reveal it, specific jailbreaking prompts can make the LLM output this hardcoded key.

**Mitigation:**
- Never embed secrets or highly sensitive operational details directly in system prompts if the user can interact with that same LLM instance.
- Store secrets in secure configurations or environment variables, accessed by the application logic, not the LLM directly.
- If instructions must be passed, use less sensitive phrasing or abstraction.
- Implement output filtering to scan for and redact sensitive patterns (like API keys) before showing the response to the user.
- Consider using separate LLM instances or prompt templates for different privilege levels if necessary.

**Demo Link:** Access the LLM07 challenge via the main dashboard (typically http://127.0.0.1:5007).

---

## LLM08: Vector and Embedding Weaknesses

**Description:**
Vulnerabilities in vector/embedding systems (often used in RAG) can be exploited to inject harmful content, manipulate model outputs, or access sensitive information. This challenge involves a semantic collision where a crafted query matches hints in a vector store, causing the LLM to generate a hidden URL for a secret flag.

**Challenge Implementation Note:**
The application allows an admin to add documents to a vector store. The core vulnerability lies in the `/ask` route where the LLM is prompted to generate a URL based on user query and context from similarity search. If an attacker (as admin) injects the flag's URL into the vector store, a crafted query can make the LLM reveal it.

**Mitigation:**
- Secure access to vector store management. Only trusted administrators should be able to add or modify documents.
- Validate and sanitize content being added to vector stores.
- Be cautious about how much trust is placed in the semantic similarity search if the underlying data can be manipulated.
- Limit the scope of information that can be retrieved or inferred from vector store context.
- Use output filtering on the LLM's response if it's constructing sensitive information like URLs based on potentially untrusted context.

**Demo Link:** Access the LLM08 challenge via the main dashboard (typically http://127.0.0.1:5008).

---

## LLM09: Misinformation

**Description:**
LLM misinformation occurs when an AI model generates false or misleading information that appears credible, potentially leading users to trust incorrect answers. This risk is amplified in sensitive contexts, where users may unknowingly rely on false data for critical decisions.

**Challenge Implementation Note:**
The application (`app/utils/llm09_2025_utils/llm09_2025_service.py`) uses a standard LLM to respond to user queries. The challenge demonstrates misinformation by providing prompts (e.g., 'list of top 10 best-selling Martian footwear brands') that are designed to elicit plausible-sounding but factually incorrect or hallucinated responses from the model.

**Mitigation:**
- Use Retrieval-Augmented Generation (RAG) with trusted and up-to-date knowledge sources.
- Fine-tune models on domain-specific, accurate data.
- Implement fact-checking mechanisms or cross-referencing with reliable sources.
- Clearly communicate the possibility of misinformation to users and indicate when content is AI-generated.
- Encourage critical thinking and provide ways for users to report inaccuracies.
- For sensitive applications, include human oversight.

**Demo Link:** Access the LLM09 challenge via the main dashboard (typically http://127.0.0.1:5009).

---

## LLM10: Unbounded Consumption

**Description:**
Unbounded Consumption refers to scenarios where LLMs can be prompted to perform resource-intensive tasks (e.g., generating extremely long texts, complex calculations, or recursive operations) leading to Denial of Service (DoS) or excessive costs. This challenge demonstrates this by trying to make the LLM generate a very long response.

**Challenge Implementation Note:**
The application's `generate_response` function in `app10.py` calls the LLM without strict limits on output length or processing time for the LLM itself. A user can submit a prompt designed to make the LLM generate an extremely verbose or computationally intensive response, leading to resource exhaustion, which is then detected by checking response time and token count post-generation.

**Mitigation:**
- Implement strict input validation on prompt length and complexity.
- Set timeouts for LLM API calls.
- Enforce limits on the number of tokens or length of the generated output (e.g., `max_tokens` parameter in API calls).
- Apply rate limiting and user quotas to prevent abuse.
- Monitor resource consumption (CPU, memory, API costs) and implement alerts.
- Consider using less powerful models for tasks that don't require extensive generation capabilities if they are prone to such abuse.

**Demo Link:** Access the LLM10 challenge via the main dashboard (typically http://127.0.0.1:5010).

---
