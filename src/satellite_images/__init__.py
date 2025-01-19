__all__ = [
    'POLYGON_COL',
    'FIELD_ID_COL',
    'DIR_NAME_COL',
    'TENANT_COL',
    'GEODF_CRS',
    'GEOM_COL',
    'DEFAULT_IMAGE_SIZE',
    'MAX_DIMENSION',
    'IMAGE_OUTPUT',
    'IMAGE_COL',
    'RESPONSE_OUTPUT',
    'RESPONSE_COL',
    'EVAL_SCRIPT_VI',
    'FIELDS_QUERY',
    'DEST_TABLE',
    'SRC_SCHEMA',
    'DEST_SCHEMA',
    'CREATED_DATE',
    'INDEX_COL'
]

POLYGON_COL = 'field_polygon_wkt'
FIELD_ID_COL = 'field_id'
DIR_NAME_COL = 'field_id_agro_organization_id'
TENANT_COL = 'agro_organization_id'
GEODF_CRS = 'EPSG:4326'
GEOM_COL = 'geometry'
DEFAULT_IMAGE_SIZE = [512, 512]
MAX_DIMENSION = 2500
IMAGE_OUTPUT = 'response.tiff'
IMAGE_COL = 'image_path'
RESPONSE_OUTPUT = 'request.json'
RESPONSE_COL = 'response_meta_path'
DEST_TABLE = 'satellite_metadata'
SRC_SCHEMA = 'management'
DEST_SCHEMA = 'landing'
CREATED_DATE = 'created_on'
INDEX_COL = 'sat_metadata_id'


EVAL_SCRIPT_VI = """
    //VERSION=3

    function setup() {
        return {
            input: [{
                bands: ["B04", "B08"]
            }],
            output: {
                bands: 3
            }
        };
    }

    function evaluatePixel(sample) {
        return [sample.B04, sample.B08];
    }
    """

# noinspection SqlNoDataSourceInspection
FIELDS_QUERY = '''
    SELECT 
        f.field_id,
        f.agro_organization_id,
        f.field_name,
        f.field_polygon_wkt
    FROM 
        management.fields f
    '''
