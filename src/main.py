import logging
from sys import exit

from src.dem.dem_images import SentinelHubDEMImages
from src.utils.paths import SENTINEL_CONFIGS
from src.utils.connector import DatabaseConnector

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('main')


db_connector = DatabaseConnector()

data = SentinelHubDEMImages(
    config_path=SENTINEL_CONFIGS,
    connector=db_connector
)


if __name__ == "__main__":
    try:
        data.get_dem_images()
    except Exception as e:
        logger.critical('Unhandled exception occurred.', exc_info=e)
        exit(-1)
