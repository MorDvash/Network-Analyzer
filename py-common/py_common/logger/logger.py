import logging


def create_logger():
    logging.basicConfig(
        format='%(levelname)s: %(name)s %(asctime)s %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S',
        level=logging.INFO)
