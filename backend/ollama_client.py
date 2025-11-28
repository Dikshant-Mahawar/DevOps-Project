import requests
from knowledge_base import query_context
import os

# Ollama API URL and credentials
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_USER = os.getenv("OLLAMA_USER", "admin")
OLLAMA_PASS = os.getenv("OLLAMA_PASS", "SuperSafe123")

# Use your installed model
MODEL_NAME = "llama3.2"

def build_prompt(query: str):
    """Combine retrieved FAISS context with user query into a single prompt."""
    context_docs = query_context(query)
    context_text = "\n".join(context_docs) if context_docs else "No salon data found."

    prompt = f"""
You are a helpful AI receptionist for a salon. 
If customer asks some absurd question not related to Salon, answer appropriately; no need to escalate.
Always answer truthfully using the context below. 
If you don't find the answer in the context, politely say you’ll confirm with your supervisor later.

Salon Knowledge:
{context_text}

User Question:
{query}

Answer:
"""
    return prompt.strip()

def ask_ollama(prompt: str, model: str = MODEL_NAME):
    """Send prompt to Ollama API and get the model’s full text output."""
    payload = {"model": model, "prompt": prompt}

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            stream=True,
            auth=(OLLAMA_USER, OLLAMA_PASS)
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"⚠️ Could not reach Ollama API: {e}"

    answer = ""
    for line in response.iter_lines():
        if line:
            data = line.decode("utf-8")
            if '"response":"' in data:
                chunk = data.split('"response":"')[1].split('"')[0]
                answer += chunk

    return answer.strip()

def generate_answer(query: str):
    prompt = build_prompt(query)
    return ask_ollama(prompt)
