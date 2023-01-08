import logging
from os import environ
from dotenv import load_dotenv

from py_common.logger.logger import create_logger
from py_common.message_queue.controller import KafkaController
from recevier import NetworkReceiver

create_logger()
logger = logging.getLogger(__name__)
load_dotenv()

IFACE_NAME = environ.get("IFACE_NAME")
KAFKA_HOST = environ.get("KAFKA_HOST")
KAFKA_PORT = environ.get("KAFKA_PORT")
TOPIC = environ.get("TOPIC")

if __name__ == '__main__':
    logger.info('Starting network receiver')
    network_receiver = NetworkReceiver(IFACE_NAME)
    logger.info('start sniffing')
    capture = network_receiver.start_sniff()

    if len(capture) > 0:
        try:
            kafka_address = f'{KAFKA_HOST}:{KAFKA_PORT}'
            logger.debug(f'kafka_address - {kafka_address}')
            logger.debug(f'TOPIC - {TOPIC}')
            message_queue = KafkaController(kafka_address, TOPIC)
            for packet in capture.sniff_continuously(packet_count=len(capture)):
                if 'IP' in packet:
                    logger.debug(f'packet - {packet}')
                    message_queue.send_message(network_receiver.process_packet(packet))
        except Exception as e:
            logger.error(f'Error accord when trying to connect message_queue {e}')
    else:
        logger.info('Did not found any network packet')