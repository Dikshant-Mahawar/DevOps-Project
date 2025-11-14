# backend/knowledge_base.py
"""
Knowledge Base using Hugging Face embeddings + FAISS.
Purpose: retrieve relevant business info as context for the LLM.
"""

from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import json
import os

INDEX_PATH = "./data/faiss_index.bin"
META_PATH = "./data/faiss_metadata.json"

embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

if os.path.exists(INDEX_PATH) and os.path.exists(META_PATH):
    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, "r") as f:
        metadata = json.load(f)
else:
    dim = embedding_model.get_sentence_embedding_dimension()
    index = faiss.IndexFlatL2(dim)
    metadata = []


def embed_text(text: str):
    emb = embedding_model.encode([text])
    return np.array(emb).astype("float32")


def add_document(text: str):
    emb = embed_text(text)
    index.add(emb)
    metadata.append({"text": text})
    persist_index()


def persist_index():
  
    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "w") as f:
        json.dump(metadata, f, indent=2)


def query_context(query: str, top_k: int = 100):
   
    if len(metadata) == 0:
        return []

    emb = embed_text(query)
    distances, indices = index.search(emb, top_k)

    results = []
    for i in indices[0]:
        if 0 <= i < len(metadata):
            results.append(metadata[i]["text"])
    return results


def seed_knowledge():
    docs = [
        "Basic haircut for men costs $20.",
        "Haircut and styling for women starts at $30.",
        "Hair coloring services range from $50 to $120 depending on length.",
        "Hair wash and scalp massage costs $10.",
        "Salon is open from 9 AM to 6 PM, Monday through Saturday.",
        "Located at 123 Main Street, Springfield."
    ]
    for doc in docs:
        add_document(doc)
    print("Seeded FAISS with sample salon knowledge.")
