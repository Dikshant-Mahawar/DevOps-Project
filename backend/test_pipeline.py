from knowledge_base import seed_knowledge, query_context
from ollama_client import generate_answer

print("Seeding FAISS knowledge base..")
seed_knowledge()

print("\nRetrieving context for: 'How much is a haircut for men?'")
print(query_context("How much is a haircut for men?"))

print("\nQuerying Ollama model:")
response = generate_answer("How much is a haircut for men?")
print("\n Model Answer:\n", response)
