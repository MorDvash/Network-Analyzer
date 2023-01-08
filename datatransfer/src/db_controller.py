import logging

from neo4j import GraphDatabase

logger = logging.getLogger(__name__)

class Neo4jController:

    def __init__(self, url: str, user: str, password: str):
        """
        :param url: url of the DB.
        :param user: DB username.
        :param password: DB password.
        """
        try:
            logger.info('initiate Neo4j driver')
            self._driver = GraphDatabase.driver(url, auth=(user, password))
        except Exception as e:
            logger.error("Failed to create the driver:", e)

    def __del__(self):
        if self._driver is not None:
            logger.info('close connection Neo4j driver')
            self._driver.close()

    def run_query(self, query: str, properties):
        """
        Running query on the DB.
        :return: result of the query
        """
        assert self._driver is not None, "Driver not initialized!"

        with self._driver.session() as session:
            logger.info(f'running query - {query}')
            try:
                result = session.run(query, properties=properties)
                return result
            except Exception as e:
                logger.error("Failed to run the query:", e)
                raise