import requests
from knowledge_base import query_context

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"   

def build_prompt(query: str):
    """Combine retrieved FAISS context with user query into a single prompt."""
    context_docs = query_context(query)
    context_text = "\n".join(context_docs) if context_docs else "No salon data found."

    prompt = f"""
You are a helpful AI receptionist for a salon. 
If customer ask some absurd question not related to Salon. Directly give appropriate answer according to you, no need to send request to Supervisor.
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
    """Send prompt to local Ollama API and get the model’s full text output."""
    payload = {"model": model, "prompt": prompt}

    response = requests.post(OLLAMA_URL, json=payload, stream=True)
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
