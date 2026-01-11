# app/config/dag_config.py

import os
from datetime import datetime


class DAGConfig:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    
    kafka_producer_dir = os.path.join(parent_dir, "kafka")
    spark_consumer_dir = os.path.join(parent_dir, "spark")
    
    ARGS = {"owner": "airflow", "start_date": datetime(2024, 10, 1) , "retries": 1}
    '''
    PRODUCER_BASH_COMMAND = rf"python {kafka_producer_dir}/producer.py"
    CONSUMER_BASH_COMMAND = rf"spark-submit {spark_consumer_dir}/consumer.py"
    '''
    '''
    PRODUCER_BASH_COMMAND = rf"python3 {kafka_producer_dir}/producer.py"
    CONSUMER_BASH_COMMAND = rf"python3 {spark_consumer_dir}/consumer.py"
    '''
    
    PRODUCER_BASH_COMMAND = """
    export PYTHONPATH=/mnt/c/Belgelerim/Code\ Repository/af-k8-kafka:$PYTHONPATH;
    python3 /mnt/c/Belgelerim/Code\ Repository/af-k8-kafka/app/kafka/producer.py
    """
    CONSUMER_BASH_COMMAND = """
    export PYTHONPATH=/mnt/c/Belgelerim/Code\ Repository/af-k8-kafka:$PYTHONPATH;
    spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1 /mnt/c/Belgelerim/Code\ Repository/af-k8-kafka/app/spark/consumer.py
    """
    
    
    #PRODUCER_BASH_COMMAND = """cd /mnt/c/Belgelerim/Code\\ Repository/af-k8-kafka && export PYTHONPATH=$(pwd):$PYTHONPATH && ./start_kafka.sh"""
    #CONSUMER_BASH_COMMAND = """cd /mnt/c/Belgelerim/Code\\ Repository/af-k8-kafka && export PYTHONPATH=$(pwd):$PYTHONPATH && ./start_spark.sh"""
    