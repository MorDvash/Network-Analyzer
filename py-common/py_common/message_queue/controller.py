import logging
from typing import Dict, List

from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaTimeoutError
from json import dumps
import json


logger = logging.getLogger(__name__)


class KafkaController:
    """
    UR implementation to Kafka controller.
    we are using kafka-python library for this controller.
    """

    def __init__(self, bootstrap_servers: str, topic: str, **kwargs: None):
        """
        :param bootstrap_servers: server address to connect.
        :param topic: topic to store the messages
        """
        self.topics = topic
        try:
            logger.info('initiate Kafka controller')
            self.consumer = KafkaConsumer(topic,
                                          bootstrap_servers=[bootstrap_servers],
                                          auto_offset_reset='earliest',  # start consuming from the earliest message
                                          enable_auto_commit=True,)
            self.producer = KafkaProducer(bootstrap_servers=[bootstrap_servers],
                                          value_serializer=lambda x:
                                          dumps(x).encode('utf-8'))
            if self.producer.bootstrap_connected() is False or self.consumer.bootstrap_connected() is False:
                raise Exception('Could not connect')

        except Exception as e:
            logger.error(f'Error accord when trying to connect: {e}')
            raise

    def __del__(self):
        try:
            self.consumer.close()
            self.producer.close()
        except Exception as e:
            logger.error(f'Error accord when trying to close connection: {e}')

    def send_message(self, message: Dict):
        """
        Send a message to Kafka
        :param message: data to send to Kafka.
        """
        try:
            self.producer.send(self.topics, value=message)
        except (Exception, KafkaTimeoutError) as e:
            logger.error(f'Error accord when sending message to Kafka: {e}')


    def get_message(self) -> List:
        record_list = []
        try:
            records = self.consumer.poll(timeout_ms=5000) # timeout in millis , here set to 1 min
            if not records:
                return []

            for tp, consumer_records in records.items():
                for consumer_record in consumer_records:
                    record_list.append(json.loads(consumer_record.value))

        except Exception as e:
            logger.error(f'Error accord when trying to receive message from Kafka: {e}')

        return  record_list