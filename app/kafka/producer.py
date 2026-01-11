# app/kafka/producer.py

from kafka import KafkaProducer
import json
import random
import time
import logging
from app.config.kafka_config import KafkaConfig
from app.config.download_config import DownloadConfig
from app.utils.json_reader import JsonReader

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

class Producers:
    def __init__(self, producer: KafkaProducer) -> None:
        self.producer = producer

    def send_random_review(self):
        try:
            json_reader = JsonReader(DownloadConfig.USER_REVIEWS_PATH)
            review = random.choice(json_reader.read_json_with_line())
            self.producer.send("reviews-topic", review)
            logger.info(f"Data sent successfully: {review['asin']}")
        except Exception as e:
            logger.error(f"Error sending data: {str(e)}")


producer = KafkaProducer(
    bootstrap_servers=KafkaConfig.BOOTSTRAP_SERVERS, 
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)


while True:
    Producers(producer=producer).send_random_review()
    time.sleep(5) 

producer.close()
