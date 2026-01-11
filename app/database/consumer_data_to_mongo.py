# app/database/consumer_data_to_mongo.py

import json
from pymongo.mongo_client import MongoClient
from app.config.database_config import DatabaseConfig
from pyspark.sql.types import StructType
import logging

class LoadData2DB:
    @staticmethod
    def load_data_to_db(client: MongoClient, consumer_data: StructType):
        try:
            db = client[DatabaseConfig.DB_NAME]
            collection = db[DatabaseConfig.STREAMING_COLLECTION_NAME]

            records = consumer_data.toJSON().collect()
            documents = [json.loads(record) for record in records]

            if documents:
                collection.insert_many(documents)
                logging.info(f"{len(documents)} records successfully added to MongoDB.")
            else:
                logging.info("No data found to insert.")

        except Exception as e:
            print(f"An error occurred while inserting data: {e}")
        finally:
            if client:
                client.close()
                


