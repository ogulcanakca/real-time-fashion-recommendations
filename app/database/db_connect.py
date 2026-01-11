# app/database/db_connect.py

from pymongo.mongo_client import MongoClient


class DBConnect:
    def connect(uri: str, client: MongoClient):
        try:
            client.admin.command("ping")
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)
