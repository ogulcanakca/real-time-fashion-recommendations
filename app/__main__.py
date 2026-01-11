# app/__main__.py

from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient
from app.database.db_connect import DBConnect
from app.database.dataset_to_mongo import LoadData2DB

from torch_geometric.data import Data
from app.models.gnn.gnn_pipeline import GraphSAGEPipeline
import torch
import numpy as np
from app.models.gnn.UGraphSAGE import GNN
from app.config.database_config import DatabaseConfig
from app.config.download_config import DownloadConfig
from app.config.model_g_config import ModelGConfig
from app.utils.downloader_gdrive import DownloaderDrive
from app.utils.json_reader import JsonReader
import os
import networkx as nx
from app.utils.choose_asin import ASIN_Getter
from app.utils.recommend_products import ProductRecommender
from app.utils.plot_images import PlotImages
import pickle
import subprocess
import time
from kafka.admin import KafkaAdminClient
from kafka.errors import KafkaError


def db_connect():
    uri = DatabaseConfig.URI

    client = MongoClient(uri, server_api=ServerApi("1"), tls=True, tlsAllowInvalidCertificates=True)
    DBConnect.connect(uri=uri, client=client)
    return client


def download_data(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    downloader = DownloaderDrive(
        link_id=DownloadConfig.REDUCED_KEYWORDS_LINK_ID,
        output_path=DownloadConfig.REDUCED_KEYWORDS_PATH,
    )
    downloader.download()
    json_reader = JsonReader(DownloadConfig.REDUCED_KEYWORDS_PATH)
    reduced_keywords = json_reader.read_json_with_load()

    downloader = DownloaderDrive(
        link_id=DownloadConfig.META_PRODUCT_LINK_ID,
        output_path=DownloadConfig.META_PRODUCT_VIEW_PATH,
    )
    downloader.download()
    json_reader = JsonReader(DownloadConfig.META_PRODUCT_VIEW_PATH)
    meta_product_view = json_reader.read_json_with_line()
    return reduced_keywords, meta_product_view


def model_and_G_pipeline(output_dir, reduced_keywords):
    model_path = os.path.join(output_dir, ModelGConfig.MODEL_PATH)
    embeddings_path = ModelGConfig.EMBEDDINGS_PATH

    if (
        not os.path.exists(model_path)
        and not os.path.exists(embeddings_path)
        and not os.path.exists(ModelGConfig.GNN_GRAPH)
    ):
        G = nx.Graph()
        gnn_pipeline = GraphSAGEPipeline()
        G = gnn_pipeline.edge_creater(reduced_keywords=reduced_keywords, G=G)
        G = gnn_pipeline.node_creater(reduced_keywords=reduced_keywords, G=G)

        node_features = torch.tensor(
            np.array([G.nodes[node]["embedding"] for node in G.nodes()]),
            dtype=torch.float,
        )
        edge_index = (
            torch.tensor(
                [[list(G.nodes).index(u), list(G.nodes).index(v)] for u, v in G.edges],
                dtype=torch.long,
            )
            .t()
            .contiguous()
        )

        with open(ModelGConfig.GNN_GRAPH, "wb") as f:
            pickle.dump(G, f)

        in_channels = node_features.shape[1]
        hidden_channels = 128
        out_channels = in_channels
        model = GNN(
            in_channels=in_channels,
            hidden_channels=hidden_channels,
            out_channels=out_channels,
        )
        data = Data(x=node_features, edge_index=edge_index)
        model = gnn_pipeline.run_model(data=data, model=model)
        node_embeddings = gnn_pipeline.evaluate_model(model=model, data=data)
    else:
        model = torch.load(model_path,weights_only=False)
        node_embeddings = torch.load(embeddings_path,weights_only=False)

        with open(ModelGConfig.GNN_GRAPH, "rb") as f:
            G = pickle.load(f)
    return G, node_embeddings

def check_kafka_connection():
    max_retries = 5
    for i in range(max_retries):
        try:
            admin_client = KafkaAdminClient(bootstrap_servers=['localhost:9092'])
            admin_client.close()
            return True
        except KafkaError:
            if i < max_retries - 1:
                time.sleep(5)
            continue
    return False

def manage_airflow_dag():
    try:
        # Wait for services to be ready
        time.sleep(10)
        
        # Unpause DAG
        subprocess.run(["airflow", "dags", "unpause", "kafka_spark_pipeline"], check=True)
        time.sleep(5)
        
        # Trigger DAG
        subprocess.run([
            "airflow", "dags", "trigger", "kafka_spark_pipeline"
        ], check=True)
        
        # Wait for DAG to initialize
        time.sleep(15)
        
    except subprocess.CalledProcessError as e:
        print(f"Error managing Airflow DAG: {str(e)}")
        raise


def main():

    client = db_connect()
    LoadData2DB.load_data_to_db(client=client)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(current_dir, "outputs")

    reduced_keywords, meta_product_view = download_data(output_dir)

    G, node_embeddings = model_and_G_pipeline(output_dir, reduced_keywords)

    node_id = ASIN_Getter.get_asin(reduced_keywords=reduced_keywords)

    similar_asins = ProductRecommender.recommend_products(
        node_id=node_id,
        reduced_keywords=reduced_keywords,
        G=G,
        node_embeddings=node_embeddings,
        top_k=10,
    )

    PlotImages.plot_recommendations_with_images(
        node_id=node_id,
        recommended_asins=similar_asins,
        meta_product_review=meta_product_view,
        top_k=10,
    )


if __name__ == "__main__":

    if not check_kafka_connection():
        print("Error: Kafka is not ready")
        exit(1)
        
    manage_airflow_dag()

    main()

