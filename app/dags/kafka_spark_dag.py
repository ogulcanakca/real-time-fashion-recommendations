from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor
from datetime import datetime, timedelta

class KafkaSparkPipeline:
    def __init__(self):
        self.default_args = {
            'owner': 'airflow',
            'depends_on_past': False,
            'email_on_failure': False,
            'email_on_retry': False,
            'retries': 3,
            'retry_delay': timedelta(minutes=1),
            'retry_exponential_backoff': True,
            'max_retry_delay': timedelta(minutes=10)
        }
        
        self.dag = DAG(
            'kafka_spark_pipeline',
            default_args=self.default_args,
            description='Kafka - Spark Streaming Pipeline',
            schedule_interval='@daily',
            start_date=datetime(2024, 12, 1),
            catchup=False,
            tags=['kafka', 'spark']
        )
        
        self.setup_tasks()
        
    def setup_tasks(self):
        # Health check for Kafka
        self.kafka_health_check = BashOperator(
            task_id='kafka_health_check',
            bash_command='echo "Checking Kafka..." && nc -zv localhost 9092',
            dag=self.dag
        )
        
        # Producer task with proper environment setup
        self.producer_task = BashOperator(
            task_id='start_kafka_producer',
            bash_command='''
                export PYTHONPATH=/mnt/c/Belgelerim/Code\ Repository/af-k8-kafka:$PYTHONPATH && \
                python3 /mnt/c/Belgelerim/Code\ Repository/af-k8-kafka/app/kafka/producer.py
            ''',
            dag=self.dag,
            env={
                'PYTHONPATH': '/mnt/c/Belgelerim/Code Repository/af-k8-kafka:${PYTHONPATH}'
            }
        )
        
        # Spark Streaming consumer task
        self.consumer_task = BashOperator(
            task_id='start_spark_streaming',
            bash_command='''
                export PYTHONPATH=/mnt/c/Belgelerim/Code\ Repository/af-k8-kafka:$PYTHONPATH && \
                spark-submit \
                --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1 \
                --conf spark.sql.streaming.checkpointLocation=/tmp/checkpoint \
                /mnt/c/Belgelerim/Code\ Repository/af-k8-kafka/app/spark/consumer.py
            ''',
            dag=self.dag,
            env={
                'PYTHONPATH': '/mnt/c/Belgelerim/Code Repository/af-k8-kafka:${PYTHONPATH}'
            }
        )
        
        # Define task dependencies
        self.kafka_health_check >> self.producer_task >> self.consumer_task

# Instantiate the pipeline
pipeline = KafkaSparkPipeline()
dag = pipeline.dag