# app/models/gnn/gnn_pipeline.py

import torch
import numpy as np
import torch.nn.functional as F
import networkx as nx
from app.config.model_g_config import ModelGConfig
from app.models.transformer_models.model_lm import PtModel
import os


class GraphSAGEPipeline:
    #def __init__(self) -> None:
     #   self.pt_model = PtModel()

    def edge_creater(self, reduced_keywords, G: nx.Graph):
        for i, (asin, keywords) in enumerate(reduced_keywords.items()):
            if i < len(reduced_keywords.keys()):
                for keyword in keywords:
                    G.add_edge(asin, keyword)
        return G

    def node_creater(self, reduced_keywords, G: nx.Graph):
        node_embeddings = {}
        for asin, keywords in reduced_keywords.items():
            keyword_embeddings = PtModel().pt_model.encode(keywords)
            node_embeddings[asin] = np.mean(keyword_embeddings, axis=0)

        for node in G.nodes():
            if node in node_embeddings:
                G.nodes[node]["embedding"] = node_embeddings[node]
            else:
                keyword_embedding = PtModel().pt_model.encode([node])[0]
                G.nodes[node]["embedding"] = keyword_embedding
        return G

    def run_model(self, data, model):
        optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

        model.train()
        for epoch in range(20):
            optimizer.zero_grad()

            output = model(data.x, data.edge_index)

            loss = F.cross_entropy(output, data.x)  # Yeni loss fonksiyonu burada
            loss.backward()
            optimizer.step()

            print(f"Epoch {epoch+1}, Loss: {loss.item()}")
        model_path = ModelGConfig.MODEL_PATH
        torch.save(model.state_dict(), model_path)
        return model

    def evaluate_model(self, model, data):
        model.eval()
        with torch.no_grad():
            node_embeddings = model(data.x, data.edge_index)
        self.print_embeddings(node_embeddings)
        embeddings_path = ModelGConfig.EMBEDDINGS_PATH
        if not os.path.exists(embeddings_path):
            torch.save(node_embeddings, embeddings_path)
        return node_embeddings

    def print_embeddings(self, node_embeddings):
        print("Node Embedding Shape:", node_embeddings.shape)
