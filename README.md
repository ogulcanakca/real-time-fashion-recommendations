
# Real-Time Fashion Recommendations

A real-time product recommendation system using GraphSAGE-based Graph Neural Networks, powered by Apache Kafka and Spark Streaming for the Amazon Fashion dataset.

## Overview

This system builds a graph-based recommendation engine that processes user reviews in real-time, trains an unsupervised GraphSAGE model, and generates product recommendations based on semantic similarity of product keywords.

## Architecture

```
Data Source (JSON) → Kafka Producer → Kafka Topic → Spark Streaming Consumer → MongoDB
                                                                    ↓
                                    GraphSAGE Model ← Product Graph ← Keywords
```

### Key Components

- **Kafka Producer**: Streams random user reviews every 5 seconds
- **Spark Consumer**: Processes streams and persists to MongoDB
- **GraphSAGE Model**: Generates product embeddings from keyword graphs
- **Recommendation Engine**: Finds similar products using euclidean distance
- **Airflow DAG**: Orchestrates the entire pipeline

## Technology Stack

- **Streaming**: Apache Kafka, Apache Spark (PySpark)
- **Database**: MongoDB Atlas
- **ML Framework**: PyTorch, PyTorch Geometric
- **NLP**: Sentence Transformers (paraphrase-MiniLM-L6-v2)
- **Orchestration**: Apache Airflow
- **Graph Library**: NetworkX

## Prerequisites

- Python 3.8+
- Apache Kafka 2.12
- Apache Spark 3.3.1
- Apache Airflow
- MongoDB Atlas account
- ZooKeeper

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ogulcanakca/real-time-fashion-recommendations.git
cd real-time-fashion-recommendations
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables in `app/config/database_config.py`:
```python
DB_USERNAME = "your_username"
DB_PASSWORD = "your_password"
URI = "your_mongodb_atlas_uri"
```

## Running the Pipeline

### Step 1: Start ZooKeeper
```bash
sudo /opt/kafka/bin/zookeeper-server-start.sh /opt/kafka/config/zookeeper.properties
```

### Step 2: Start Kafka Server
```bash
sudo /opt/kafka/bin/kafka-server-start.sh /opt/kafka/config/server.properties
```

### Step 3: Set Python Path
```bash
export PYTHONPATH=/path/to/project:$PYTHONPATH
```

### Step 4: Start Kafka Producer
```bash
python3 app/kafka/producer.py
```

### Step 5: Start Spark Consumer
```bash
spark-submit   --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1,org.mongodb.spark:mongo-spark-connector_2.12:3.0.1   --conf "spark.mongodb.input.uri=mongodb://127.0.0.1:27017/AMAZON_FASHION"   --conf "spark.mongodb.output.uri=mongodb://127.0.0.1:27017/AMAZON_FASHION"   --conf "spark.mongodb.database=AMAZON_FASHION"   --conf "spark.mongodb.collection=streaming_reviews"   --conf "spark.mongodb.output.database=AMAZON_FASHION"   --conf "spark.mongodb.output.collection=streaming_reviews"   app/spark/consumer.py
```

### Alternative: Using Airflow
```bash
airflow dags unpause kafka_spark_pipeline
airflow dags trigger kafka_spark_pipeline
```

## Project Structure

```
app/
├── config/              # Configuration files
├── dags/                # Airflow DAG definitions
├── database/            # MongoDB connection and data loaders
├── kafka/               # Kafka producer implementation
├── spark/               # Spark streaming consumer
├── models/              # GNN and transformer models
│   ├── gnn/            # GraphSAGE pipeline
│   └── transformer_models/  # Sentence embeddings
├── utils/               # Helper utilities
└── outputs/             # Model artifacts and embeddings
```

## Data Flow

1. **Initial Setup**: Load user reviews from JSON to MongoDB
2. **Graph Construction**: Build product-keyword bipartite graph
3. **Node Embedding**: Generate embeddings using Sentence Transformers
4. **Model Training**: Train unsupervised GraphSAGE model (20 epochs)
5. **Stream Processing**: Kafka produces reviews, Spark consumes and stores
6. **Recommendation**: Select random product and find top-k similar items
7. **Visualization**: Display products with images using matplotlib

## Model Details

### GraphSAGE Architecture
- **Input Channels**: 384 (from Sentence Transformer)
- **Hidden Channels**: 128
- **Output Channels**: 384
- **Layers**: 2 GraphSAGE layers + BatchNorm + Linear
- **Loss Function**: Cross-entropy
- **Optimizer**: Adam (lr=0.01)

### Graph Structure
- **Nodes**: Products (ASINs) + Keywords
- **Edges**: Product-Keyword relationships
- **Node Features**: Mean of keyword embeddings per product

## Troubleshooting

### ZooKeeper Port Already in Use
```bash
# Find process using port 2181
sudo lsof -i :2181
# Kill the process
sudo kill <PID>
```

### MongoDB Connection Issues
Ensure TLS settings are properly configured:
```python
client = MongoClient(uri, tls=True, tlsAllowInvalidCertificates=True)
```

## Database Schema

### Collections

**user_reviews**: Initial dataset of user reviews
- `overall`, `verified`, `reviewTime`, `reviewerID`, `asin`, `reviewerName`, `reviewText`, `summary`, `unixReviewTime`

**streaming_reviews**: Real-time streaming data
- Same schema as user_reviews + `processing_time`

## Configuration

All configurations are centralized in `app/config/`:
- `database_config.py`: MongoDB connection settings
- `kafka_config.py`: Kafka bootstrap servers
- `spark_config.py`: Checkpoint locations
- `dag_config.py`: Airflow DAG parameters
- `model_g_config.py`: Model and embedding paths
- `download_config.py`: Google Drive file IDs

## Future Enhancements

- Implement batch recommendations for multiple users
- Add A/B testing framework
- Deploy on Kubernetes for scalability
- Add monitoring with Prometheus and Grafana
- Implement model versioning with MLflow
