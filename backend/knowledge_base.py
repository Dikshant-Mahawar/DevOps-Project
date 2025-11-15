# backend/knowledge_base.py
"""
Knowledge Base using ONNX MiniLM embeddings + FAISS
Completely torch-free, transformers-free, nltk-free.
"""

import os
import json
import faiss
import numpy as np
from huggingface_hub import hf_hub_download
import onnxruntime as ort

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INDEX_PATH = os.path.join(BASE_DIR, "data/faiss_index.bin")
META_PATH  = os.path.join(BASE_DIR, "data/faiss_metadata.json")


# ------------------------------
# Load tokenizer files (from HF)
# ------------------------------

# Download tokenizer vocab + ONNX model
VOCAB_PATH = hf_hub_download(
    repo_id="sentence-transformers/all-MiniLM-L6-v2",
    filename="tokenizer.json"
)

MODEL_PATH = hf_hub_download(
    repo_id="sentence-transformers/all-MiniLM-L6-v2",
    filename="onnx/model.onnx"
)

# Load tokenizer manually (no transformers needed)
import json
with open(VOCAB_PATH, "r") as f:
    tokenizer = json.load(f)

# Basic tokenizer: encode using WordPiece vocab
# This minimal tokenizer is enough for similarity tasks
vocab = tokenizer["model"]["vocab"]
unk_token_id = vocab.get("[UNK]", 1)

def tokenize(text):
    tokens = text.lower().split()   # simple tokenizer
    return [vocab.get(tok, unk_token_id) for tok in tokens]

# ------------------------------
# Load ONNX Runtime Session
# ------------------------------
session = ort.InferenceSession(MODEL_PATH, providers=["CPUExecutionProvider"])


def embed_text(text: str):
    ids = tokenize(text)

    input_ids = np.array([ids], dtype=np.int64)
    attention_mask = np.ones_like(input_ids, dtype=np.int64)
    token_type_ids = np.zeros_like(input_ids, dtype=np.int64)

    outputs = session.run(
        None,
        {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "token_type_ids": token_type_ids
        }
    )

    # outputs[0] is (1, seq_len, 384)
    token_embeddings = outputs[0]                 # shape: (1, seq_len, 384)
    mask = attention_mask[:, :, None]             # reshape to (1, seq_len, 1)

    # mean pooling
    summed = np.sum(token_embeddings * mask, axis=1)
    counts = np.sum(mask, axis=1)
    emb = summed / counts                         # shape: (1, 384)

    return emb.astype("float32")



# ------------------------------
# FAISS INDEX INIT
# ------------------------------

if os.path.exists(INDEX_PATH) and os.path.exists(META_PATH):
    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, "r") as f:
        metadata = json.load(f)
else:
    dim = 384  # All-MiniLM-L6-v2 ONNX embedding size
    index = faiss.IndexFlatL2(dim)
    metadata = []


def persist_index():
    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "w") as f:
        json.dump(metadata, f, indent=2)


def add_document(text: str):
    emb = embed_text(text)
    index.add(emb)
    metadata.append({"text": text})
    persist_index()


def query_context(query: str, top_k=50):
    if len(metadata) == 0:
        return []

    q_emb = embed_text(query)
    distances, indices = index.search(q_emb, top_k)

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
