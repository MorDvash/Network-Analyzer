import logging
from os import environ
from dotenv import load_dotenv

from py_common.message_queue.controller import KafkaController
from py_common.logger.logger import create_logger
from db_controller import Neo4jController

create_logger()
logger = logging.getLogger(__name__)
load_dotenv()

KAFKA_HOST = environ.get("KAFKA_HOST")
KAFKA_PORT = environ.get("KAFKA_PORT")
TOPIC = environ.get("TOPIC")
DB_URL = environ.get("DB_URL")
DB_USER = environ.get("DB_USER")
DB_PASSWORD = environ.get("DB_PASSWORD")

if __name__ == '__main__':

    kafka_address = f'{KAFKA_HOST}:{KAFKA_PORT}'
    logger.debug(f'kafka_address - {kafka_address}')
    logger.debug(f'TOPIC - {TOPIC}')
    message_queue = KafkaController(kafka_address, TOPIC)
    db = Neo4jController(DB_URL, DB_USER, DB_PASSWORD)
    while True:
        records = message_queue.get_message()
        for record in records:
            query = "CREATE (p:Packet $properties)"
            db.run_query(query, record)
            print(record)
