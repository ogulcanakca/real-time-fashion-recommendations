# app/database/dataset_to_mongo.py

import json
from pymongo.mongo_client import MongoClient
from app.config.download_config import DownloadConfig
from app.utils.json_reader import JsonReader
from app.config.database_config import DatabaseConfig


class LoadData2DB:

    @staticmethod
    def load_data_to_db(client: MongoClient):
        db = client[DatabaseConfig.DB_NAME]
        collection = db[DatabaseConfig.COLLECTION_NAME]

        if collection.estimated_document_count() > 0:
            print("Koleksiyon zaten mevcut, veri yüklenmedi.")
            return

        json_file_path = DownloadConfig.USER_REVIEWS_PATH

        try:
            data = JsonReader.read_json_with_line(json_file_path)

            if isinstance(data, list):
                collection.insert_many(data)
            else:
                collection.insert_one(data)

            print("JSON verisi başarıyla MongoDB'ye eklendi.")
        except Exception as e:
            print(f"Veri ekleme sırasında bir hata oluştu: {e}")