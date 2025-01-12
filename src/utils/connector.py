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
    """
    This class facilitates creating a connection to a database using SQLAlchemy.

    Attributes:
        logger (Logger): Logger object for logging messages.
        db_config (dict): Database configuration loaded from a YAML file.
    """

    def __init__(self):
        """
        Initializes the database configurations.

        Raises:
            FileNotFoundError: If the YAML file specified by STAGING_DB_PATH is not found.
            yaml.YAMLError: If there is an error loading the database configuration YAML file.
            Exception: If an unexpected error occurs.
        """
        self.logger = logging.getLogger(__name__)
        self.db_config = database_conn_configs()

    def get_url(self) -> str:
        """
        Create database connection string url.

        Returns:
        -------
        connection_string : str
            A database connection string url.
        """
        connection_string = f"{self.db_config['driver_name']}://" \
                            f"{os.environ['DB_USERNAME']}:" \
                            f"{os.environ['DB_PASSWORD']}@" \
                            f"{self.db_config['host']}:" \
                            f"{self.db_config['port']}/" \
                            f"{self.db_config['database']}?" \
                            f"{self.db_config['additional_options']}"
        return connection_string

    def get_engine(self) -> Engine:
        """
        Create a SQLAlchemy engine object using the database configuration.

        Returns:
        -------
        engine : Engine
            A SQLAlchemy engine object that can be used to interact with the database.

        Raises:
        ------
        Exception
            If there is an error creating the engine, this function raises an exception with the error message.
        """
        try:
            engine = create_engine(url=self.get_url())
            self.logger.info('Created database engine.')
            return engine
        except Exception as e:
            self.logger.error(f'Error creating database engine: {e}')
            raise e

    def get_session(self) -> Session:
        """
        Creates a SQLAlchemy session object for performing database operations.

        Returns:
            object: SQLAlchemy session object.
        """
        engine = self.get_engine()
        Session = sessionmaker(bind=engine)
        self.logger.info('Database connection session created.')
        return Session()
