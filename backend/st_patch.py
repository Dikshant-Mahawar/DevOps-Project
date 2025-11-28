# backend/st_patch.py
import sys
import types

# -------------------------------
# Fake torch package
# -------------------------------
fake_torch = types.ModuleType("torch")
fake_torch.__dict__["__version__"] = "0.0"
fake_torch.float32 = None
fake_torch.device = None

fake_torch.utils = types.ModuleType("utils")
fake_torch.utils.data = types.ModuleType("data")

class FakeDataset:
    pass

fake_torch.utils.data.Dataset = FakeDataset

fake_torch.nn = types.ModuleType("nn")
fake_torch.cuda = types.ModuleType("cuda")

sys.modules["torch"] = fake_torch
sys.modules["torch.utils"] = fake_torch.utils
sys.modules["torch.utils.data"] = fake_torch.utils.data
sys.modules["torch.nn"] = fake_torch.nn
sys.modules["torch.cuda"] = fake_torch.cuda

# -------------------------------
# Fake nltk base package
# -------------------------------
fake_nltk = types.ModuleType("nltk")
fake_nltk.data = types.SimpleNamespace(path=[])
sys.modules["nltk"] = fake_nltk

# -------------------------------
# Fake nltk.tokenize.treebank
# -------------------------------
fake_nltk_tokenize = types.ModuleType("nltk.tokenize")
fake_nltk_tokenize.treebank = types.ModuleType("treebank")

class FakeDetokenizer:
    def detokenize(self, tokens):
        return " ".join(tokens)

fake_nltk_tokenize.treebank.TreebankWordDetokenizer = FakeDetokenizer

sys.modules["nltk.tokenize"] = fake_nltk_tokenize
sys.modules["nltk.tokenize.treebank"] = fake_nltk_tokenize.treebank
