#app /spark/consumer.py

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, current_timestamp
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    FloatType,
    BooleanType,
)
import logging
from app.database.consumer_data_to_mongo import LoadData2DB as LoadData2DBConsumer
from pymongo.mongo_client import MongoClient
from app.config.database_config import DatabaseConfig
from pymongo.server_api import ServerApi
import certifi

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[logging.StreamHandler()]
)


logger = logging.getLogger(__name__)


class SparkKafkaStreaming:
    def __init__(self, spark: SparkSession, schema: StructType, df: StructType) -> None:
        self.spark = spark
        self.schema = schema
        self.df = df
        
    def db_connect(self):
        try:
            uri = DatabaseConfig.URI
            client = MongoClient(
            uri,
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=5000
        )
            return client
        except Exception as e:
            logger.error(f"MongoDB connection error: {e}")
            raise
        

    def foreach_batch_function(self, df, epoch_id):
        try:
            logger.info(f"Processing batch {epoch_id}")
            logger.info(f"Number of records in batch: {df.count()}")
            df.show()
            db_client = self.db_connect()
            LoadData2DBConsumer.load_data_to_db(client=db_client, consumer_data=df)
            
            
        except Exception as e:
            logger.error(f"Error in foreach_batch_function: {str(e)}", exc_info=True)

    def start_streaming(self):
        logger.debug("start_streaming function has been called.")
        try:
            reviews_df = self.df.select(
                from_json(col("value").cast("string"), self.schema).alias("data")
            ).select("data.*")

            reviews_df = reviews_df.withColumn("processing_time", current_timestamp())

            query = reviews_df.writeStream \
                .foreachBatch(self.foreach_batch_function) \
                .outputMode("append") \
                .trigger(processingTime='5 seconds') \
                .start()

            logger.info("Streaming started successfully")
            query.awaitTermination()

        except Exception as e:
            logger.error(f"Error in streaming: {str(e)}")
            raise

spark = SparkSession.builder \
    .appName("KafkaSparkStreaming") \
    .master("local[*]") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1") \
    .config("spark.sql.streaming.checkpointLocation", "/tmp/checkpoint") \
    .getOrCreate()

schema = StructType(
    [
        StructField("overall", FloatType()),
        StructField("verified", BooleanType()),
        StructField("reviewTime", StringType()),
        StructField("reviewerID", StringType()),
        StructField("asin", StringType()),
        StructField("reviewerName", StringType()),
        StructField("reviewText", StringType()),
        StructField("summary", StringType()),
        StructField("unixReviewTime", StringType()),
    ]
)

df = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "reviews-topic")
    .option("startingOffsets", "earliest")
    .load()
)

SparkKafkaStreaming(spark=spark, schema=schema, df=df).start_streaming()