# app/config/database_config.py


class DatabaseConfig:
    DB_USERNAME = "akcaogulcan"
    DB_PASSWORD = "Asdasdasd1113"
    #URI = f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@cluster0.kxko2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0&ssl=true&ssl_cert_reqs=CERT_NONE"
    URI = f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@cluster0.kxko2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0&tls=true&tlsAllowInvalidCertificates=true"
    DB_NAME = "AMAZON_FASHION"
    COLLECTION_NAME = "user_reviews"
    STREAMING_COLLECTION_NAME = "streaming_reviews"
    