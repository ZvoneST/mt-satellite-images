import logging
import os
from pandas import DataFrame, read_sql_query
from geopandas import GeoDataFrame, GeoSeries
from sentinelhub import SHConfig

from src.dem import *
from src.utils.connector import DatabaseConnector
from src.dem.geospatial_mng import GeospatialDataManager
from src.utils.source_configs import open_config_file
from src.utils.paths import IMAGES_DIR_REMOTE

logger = logging.getLogger(__name__)


class SatelliteImages(GeospatialDataManager):
    def __init__(self, config_path: str, connector: DatabaseConnector):
        super().__init__()
        self.config_path = config_path
        self.connector = connector

    def _sentinel_configs(self) -> SHConfig:
        configs = open_config_file(file_path=self.config_path)
        sentinel_config = SHConfig(**configs)
        logger.info(f"Loaded sentinelhub credentials")
        return sentinel_config

    def _get_fields(self) -> DataFrame:
        df = read_sql_query(
            sql=FIELDS_QUERY,
            con=self.connector.get_url()
        )
        logger.info(f"Getting {len(df)} fields from database")
        return df

    def _fields_geo_transform(self) -> GeoDataFrame:
        fields_df = self._get_fields()
        logger.info(f"Transforming fields to geo data")
        fields_df[POLIGON_COL] = GeoSeries.from_wkt(fields_df[POLIGON_COL], crs=GEODF_CRS)
        fields_df.rename(columns={POLIGON_COL: GEOM_COL}, inplace=True)
        geo_fields = GeoDataFrame(fields_df, geometry=GEOM_COL)
        geo_fields[DIR_NAME_COL] = ['_'.join([str(i), str(n)])
                                    for i, n in zip(geo_fields[FIELD_ID_COL], geo_fields[TENANT_COL])]
        return geo_fields

    def get_dem_images(self):
        configs = self._sentinel_configs()
        geo_data = self._fields_geo_transform()
        directories = self.get_dir_names(geo_df=geo_data)
        date_from, date_to = self.get_dates()
        logger.info('Downloading DEM images')
        fields_ids = list()
        image_paths = list()
        response_paths = list()

        for directory in directories:
            dir_path = os.path.join(IMAGES_DIR_REMOTE, directory)
            os.makedirs(dir_path, exist_ok=True)

            polygon_wkt = geo_data[geo_data[DIR_NAME_COL] == directory].iloc[0][GEOM_COL]
            bbox, size, geometry = self.get_geo_metadata(polygon=polygon_wkt, field_tenant=directory)

            self.dem_image_request(
                sh_config=configs,
                eval_script=EVALSCRIPT_DEM,
                date_from=date_from,
                date_to=date_to,
                bbox=bbox,
                size=size,
                geometry=geometry,
                dir_path=dir_path
            )

            for response_num in os.listdir(dir_path):
                meta_path = os.path.join(IMAGES_DIR_REMOTE, directory, response_num, RESPONSE_OUTPUT)
                image_path = os.path.join(IMAGES_DIR_REMOTE, directory, response_num, IMAGE_OUTPUT)
                fields_ids.append(int(directory.split('_')[0]))
                image_paths.append(image_path)
                response_paths.append(meta_path)

        logger.info('Importing meta data into database')
        self.store_image_paths(
            url=self.connector.get_url(),
            field_id_data=fields_ids,
            image_paths_data=image_paths,
            response_paths_data=response_paths
        )
