# app/models/transformer_models/model_lm.py

from sentence_transformers import SentenceTransformer


class PtModel:
    pt_model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
