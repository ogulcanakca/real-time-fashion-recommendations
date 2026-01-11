# app/config/model_g_config.py

import os


class ModelGConfig:

    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    outputs_dir = os.path.join(parent_dir, "outputs")
    MODEL_PATH = rf"{outputs_dir}\model\unsupervised_graphsage_model.pth"
    EMBEDDINGS_PATH = rf"{outputs_dir}\embedding\node_embeddings.pt"
    GNN_GRAPH = rf"{outputs_dir}\graph\gnn_graph.gpickle"
