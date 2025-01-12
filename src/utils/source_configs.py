import logging
import yaml

from src.utils.paths import *

__all__ = [
    'open_config_file',
    'database_conn_configs'
]

logger = logging.getLogger(__name__)


def open_config_file(file_path: str):
    with open(file_path, 'r') as file:
        try:
            logger.info(f'Getting config file for sentinel creds')
            configs_file = yaml.load(file, Loader=yaml.FullLoader)
            return configs_file
        except FileNotFoundError as e:
            logger.error(f'File not found at path: {file_path}')
            raise e
        except yaml.YAMLError as e:
            logger.error(f'Error parsing config file: {e}')
            raise e
        except Exception as e:
            logger.error(f'An unexpected error occurred: {e}')
            raise e


def database_conn_configs():
    with open(SOURCE_CONFIGS, "r") as db:
        try:
            db_config = yaml.load(db, Loader=yaml.FullLoader)
            logger.info(f'Database connection protocol defined')
            return db_config
        except FileNotFoundError as e:
            logger.error(f'File not found at path: {SOURCE_CONFIGS}')
            raise e
        except yaml.YAMLError as e:
            logger.error(f'Error loading db config YAML file: {e}')
            raise e
        except Exception as e:
            logger.error(f'An unexpected error occurred: {e}')
            raise e
