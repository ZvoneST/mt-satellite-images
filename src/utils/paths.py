import os

__all__ = [
    'SOURCE_CONFIGS',
    'SENTINEL_CONFIGS',
    'IMAGES_DIR_REMOTE'
]

_ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
_CONFIGS_DIR = os.path.join(_ROOT_DIR, 'configs')

SOURCE_CONFIGS = os.path.join(_CONFIGS_DIR, 'db_source.yml')
SENTINEL_CONFIGS = os.path.join(_CONFIGS_DIR, 'sentinel.yml')

IMAGES_DIR_REMOTE = '/home/cladmin/Downloads/DEM/'
