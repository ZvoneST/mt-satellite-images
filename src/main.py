import logging
from sys import exit

from satellite_images.satellite_images import SatelliteImages
from utils.paths import SENTINEL_CONFIGS
from utils.connector import DatabaseConnector

SOURCE_LABEL = 'src'
DESTINATION_LABEL = 'dest'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('main')


src_conn = DatabaseConnector(db_label=SOURCE_LABEL)
dest_conn = DatabaseConnector(db_label=DESTINATION_LABEL)

data = SatelliteImages(
    src_con=src_conn,
    dest_con=dest_conn
)


if __name__ == "__main__":
    try:
        data.get_satellite_images()
    except Exception as e:
        logger.critical('Unhandled exception occurred.', exc_info=e)
        exit(-1)
