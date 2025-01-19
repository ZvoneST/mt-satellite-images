import logging
import os

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from src.utils.source_configs import database_conn_configs

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class DatabaseConnector:

    def __init__(self, db_label: str):
        self.logger = logging.getLogger(__name__)
        self.db_config = database_conn_configs(db=db_label)

    def get_url(self) -> str:
        connection_string = f"{self.db_config['driver_name']}://" \
                            f"{os.environ['DB_USERNAME']}:" \
                            f"{os.environ['DB_PASSWORD']}@" \
                            f"{os.environ['HOST']}:" \
                            f"{self.db_config['port']}/" \
                            f"{self.db_config['database']}?"
        return connection_string

    def get_engine(self) -> Engine:
        try:
            engine = create_engine(url=self.get_url())
            self.logger.info('Created database engine.')
            return engine
        except Exception as e:
            self.logger.error(f'Error creating database engine: {e}')
            raise e

    def get_session(self) -> Session:
        engine = self.get_engine()
        Session = sessionmaker(bind=engine)
        self.logger.info('Database connection session created.')
        return Session()
