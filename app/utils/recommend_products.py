# app/utils/recommend_products.py

import torch
import numpy as np
from scipy.spatial.distance import cdist


class ProductRecommender:
    @staticmethod
    def euclidean_distance(embedding, other_embeddings):
        return cdist(
            embedding.unsqueeze(0).cpu(), other_embeddings.cpu(), metric="euclidean"
        ).squeeze()

    @staticmethod
    def recommend_products(node_id, reduced_keywords, G, node_embeddings, top_k=10):
        node_index = list(G.nodes()).index(node_id)

        product_nodes = [n for n in G.nodes() if n in reduced_keywords.keys()]
        embedding = node_embeddings[node_index]

        product_embeddings = torch.tensor(
            np.array([G.nodes[asin]["embedding"] for asin in product_nodes])
        )

        similarities = ProductRecommender.euclidean_distance(
            embedding, product_embeddings
        )

        similar_node_indices = np.argsort(similarities)
        similar_node_indices = [
            i for i in similar_node_indices if product_nodes[i] != node_id
        ][:top_k]

        similar_asins = [product_nodes[i] for i in similar_node_indices]

        print(f"Keywords for ASIN {node_id}: {reduced_keywords[node_id]}")
        for asin in similar_asins:
            print(f"Keywords for ASIN {asin}: {reduced_keywords[asin]}")

        return similar_asins
