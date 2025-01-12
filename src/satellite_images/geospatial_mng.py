import logging
from typing import List, Tuple
from datetime import date, timedelta
from geopandas import GeoDataFrame
from pandas import DataFrame
from requests import HTTPError
from shapely import Polygon
from sentinelhub import (CRS, BBox, bbox_to_dimensions, Geometry,
                         SentinelHubRequest, DataCollection, MimeType, SHConfig)

from src.dem import (DIR_NAME_COL, FIELD_ID_COL, IMAGE_COL, RESPONSE_COL,
                     DB_TABLE, DB_SCHEMA, INDEX_COL, DEFAULT_IMAGE_SIZE, MAX_DIMENSION)

logger = logging.getLogger(__name__)


class GeospatialDataManager:
    @staticmethod
    def get_geo_metadata(
            polygon: Polygon,
            field_tenant: str,
            image_size: bool = False
    ) -> Tuple[BBox, Tuple[float, float], GeoDataFrame] | Tuple[BBox, GeoDataFrame]:
        bbox = BBox(bbox=polygon.bounds, crs=CRS.WGS84)
        geometry = Geometry(geometry=polygon, crs=CRS.WGS84)
        if not image_size:
            size = bbox_to_dimensions(bbox, resolution=1)  # Example resolution
            if size[0] > MAX_DIMENSION or size[1] > MAX_DIMENSION:
                logger.warning(f'Image size for {field_tenant} is grater than {MAX_DIMENSION}. '
                               f'Implementing image resizing for {field_tenant}')
                aspect_ratio = size[0] / size[1]
                if aspect_ratio > 1:
                    new_width = MAX_DIMENSION
                    new_height = int(MAX_DIMENSION / aspect_ratio)
                else:
                    new_height = MAX_DIMENSION
                    new_width = int(MAX_DIMENSION * aspect_ratio)
                size = (new_width, new_height)
            return bbox, size, geometry
        else:
            return bbox, DEFAULT_IMAGE_SIZE, geometry

    @staticmethod
    def get_dir_names(geo_df: GeoDataFrame) -> List[str]:
        return geo_df[DIR_NAME_COL].unique().tolist()

    @staticmethod
    def get_dates() -> tuple[date, date]:
        date_from = date.today() - timedelta(days=10)
        date_to = date.today() - timedelta(days=9)
        return date_from, date_to

    @staticmethod
    def dem_image_request(
            sh_config: SHConfig,
            eval_script: str,
            date_from: date,
            date_to: date,
            bbox: BBox,
            size: Tuple[int, int],
            geometry: GeoDataFrame,
            dir_path: str

    ):
        try:
            request_image = SentinelHubRequest(
                evalscript=eval_script,
                input_data=[
                    SentinelHubRequest.input_data(
                        data_collection=DataCollection.DEM,
                        time_interval=(date_from, date_to)
                    )
                ],
                responses=[
                    SentinelHubRequest.output_response(
                        identifier='default',
                        response_format=MimeType.TIFF
                    )
                ],
                bbox=bbox,
                size=size,
                geometry=geometry,
                config=sh_config,
                data_folder=dir_path
            )
            request_image.save_data()
        except HTTPError as e:
            logger.error(f'Bad request: {e.response}')
            raise e
        except Exception as e:
            logger.error(f'Unexpected error occurred: {e}')

    @staticmethod
    def store_image_paths(
            url: str,
            field_id_data: List[int],
            image_paths_data: List[str],
            response_paths_data: List[str]
    ):
        metadata_df = DataFrame(
            data={
                FIELD_ID_COL: field_id_data,
                IMAGE_COL: image_paths_data,
                RESPONSE_COL: response_paths_data
            }
        )
        metadata_df.to_sql(
            name=DB_TABLE,
            con=url,
            schema=DB_SCHEMA,
            if_exists='append',
            index_label=INDEX_COL,
            index=False
        )
