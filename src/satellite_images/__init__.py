__all__ = [
    'POLIGON_COL',
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
    'EVALSCRIPT_DEM',
    'FIELDS_QUERY',
    'DB_TABLE',
    'DB_SCHEMA',
    'CREATED_DATE',
    'INDEX_COL'
]

POLIGON_COL = 'PoligonWKT'
FIELD_ID_COL = 'FieldId'
DIR_NAME_COL = 'FieldID_TenantID'
TENANT_COL = 'TenantId'
GEODF_CRS = 'EPSG:4326'
GEOM_COL = 'geometry'
DEFAULT_IMAGE_SIZE = [512, 512]
MAX_DIMENSION = 2500
IMAGE_OUTPUT = 'response.tiff'
IMAGE_COL = 'ImageDEMPath'
RESPONSE_OUTPUT = 'request.json'
RESPONSE_COL = 'ResponseMetaPath'
DB_TABLE = 'PathsToDEM'
DB_SCHEMA = 'dbo'
CREATED_DATE = 'CreatedOn'
INDEX_COL = 'PathsToDEMId'


EVALSCRIPT_DEM = """
        //VERSION=3
        function setup() {
          return {
            input: ["DEM"],
            output:{
              id: "default",
              bands: 1,
              sampleType: SampleType.FLOAT32
            }
          }
        }
        
        function evaluatePixel(sample) {
          return [sample.DEM]
        }
"""

FIELDS_QUERY = '''
        SELECT 
            f.FieldId
            ,f.TenantId
            ,f.PoligonWKT
        FROM 
            dbo.Fields AS f
        LEFT JOIN 
            dbo.PathsToDEM AS dem 
            ON f.FieldId = dem.FieldId
        WHERE 
            f.PoligonWKT IS NOT NULL
            AND f.TenantId != 0
            AND dem.FieldId IS NULL;
    '''
