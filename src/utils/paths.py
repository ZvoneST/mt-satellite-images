import os

__all__ = [
    'SOURCE_CONFIGS',
    'DESTINATION_CONFIGS',
    'IMAGES_DIR'
]

_ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
_CONFIGS_DIR = os.path.join(_ROOT_DIR, 'configs')

SOURCE_CONFIGS = os.path.join(_CONFIGS_DIR, 'db_source.yml')
DESTINATION_CONFIGS = os.path.join(_CONFIGS_DIR, 'db_destination.yml')

IMAGES_DIR = '/home/mtsi/sentinel_images/landing/'
MD_IMAGE_DIR = '/home/zvone/mtsi/sentinel_images/landing/'
