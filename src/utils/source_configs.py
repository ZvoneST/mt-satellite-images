import logging
import os

import yaml

from src.utils.paths import *
from sentinelhub import SHConfig

__all__ = [
    'sentinel_configs',
    'database_conn_configs'
]

logger = logging.getLogger(__name__)


def sentinel_configs() -> SHConfig:
    configs =  {'instance_id': os.environ['SH_INSTANCE'],
                'sh_client_id': os.environ['SH_CLIENT_ID'],
                'sh_client_secret': os.environ['SH_CLIENT_SECRET']}
    sat_configs = SHConfig(**configs)
    logger.info(f"Loaded sentinelhub credentials")
    return sat_configs


def database_conn_configs(db: str):
    if db == 'src':
        db_configs = SOURCE_CONFIGS
    else:
        db_configs = DESTINATION_CONFIGS

    with open(db_configs, "r") as db:
        try:
            db_config = yaml.load(db, Loader=yaml.FullLoader)
            logger.info(f'Database connection protocol defined')
            return db_config
        except FileNotFoundError as e:
            logger.error(f'File not found at path: {db_configs}')
            raise e
        except yaml.YAMLError as e:
            logger.error(f'Error loading db config YAML file: {e}')
            raise e
        except Exception as e:
            logger.error(f'An unexpected error occurred: {e}')
            raise e
