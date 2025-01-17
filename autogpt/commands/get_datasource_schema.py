import yaml
import os
from enum import Enum
from collections import defaultdict
import pandas as pd

RELATIVE_FILE_PATH = 'datasources/datasources.yml'

# Data source types


class DataSourceType(Enum):
    BLOB_STORAGE_URL = 'blob_storage_url'
    SNOWFLAKE = 'snowflake'
    # Add more datasource types as needed


# Classes representing database metadata

class TableSchema:
    """
    Class to represent a database table with columns.
    """

    def __init__(self, name):
        self.name = name
        self.columns = {}

    def add_column(self, col_name: str, col_type: str):
        """
        Add a column to the table.
        """
        self.columns[col_name] = col_type

    def __str__(self):
        return f"Table(name={self.name}, columns={str(self.columns)})"


class DatabaseSchema:
    """
    Class to represent a database with tables.
    """

    def __init__(self, name):
        self.name = name
        self.tables = []

    def add_table(self, tbl: TableSchema):
        self.tables.append(tbl)

    def __str__(self):
        tables_repr = [str(tbl) for tbl in self.tables]
        return f"Database(name={self.name}, tables={tables_repr})"

#########################################################

# handling yaml file


def get_datasource_yaml_path():
    """get abs path to yaml file"""
    path = os.path.abspath(__file__)
    dir = os.path.dirname(path)

    return os.path.join(dir, RELATIVE_FILE_PATH)


def read_yaml_file(file_path):
    """read yaml file to dict"""
    with open(file_path, 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    return config


def map_datasource_config_by_type(yaml_config: dict) -> dict[DataSourceType, list]:
    # map data source connections by type
    ds_cfg_map = defaultdict(list)
    for config in yaml_config["data_sources"]:
        if 'type' in config and config['type'] == DataSourceType.BLOB_STORAGE_URL.value:
            # Notice here key is the enum var not string value
            ds_cfg_map[DataSourceType.BLOB_STORAGE_URL].append(config)

    return ds_cfg_map

# read out data sources schema


def read_datasources(ds_cfg_map: dict[DataSourceType, list]) -> list[DatabaseSchema]:

    # Each datasource is parsed into a Database class
    # dict format: {datasource name: Database class}
    db_schemas = []

    # handling blob storage url sources
    for cfg in ds_cfg_map[DataSourceType.BLOB_STORAGE_URL]:
        if 'url' not in cfg:
            print(f"URL not specified for blob url datasource {str(cfg)}, skipped...")
            continue
        url = cfg['url']

        # if it's parquet file
        if url.endswith('.parquet'):
            db_schemas.append(read_parquet_schema(cfg['name'], url))
        else:
            print(f"Unsupported blob url datasource file type {str(cfg)}, skipped...")

    return db_schemas


# read parquet file and populate schema
def read_parquet_schema(source_name: str, url: str) -> DatabaseSchema:
    # Read the Parquet file using pandas
    df = pd.read_parquet(url)

    # Parse the schema from the DataFrame
    db_schema = DatabaseSchema(source_name)
    tbl_schema = TableSchema(source_name)

    # Loop through the columns in the DataFrame
    for col_name, col_type in df.dtypes.items():
        tbl_schema.add_column(col_name, str(col_type))  # Add column to the table schema

    db_schema.add_table(tbl_schema)  # Add table to the database schema

    return db_schema


# read scan understand data sources

def get_datasource_schema() -> str:
    """ read datasources from a YAML file.
        return data source schemas in a string
    """
    config = read_yaml_file(get_datasource_yaml_path())

    ds_cfg_map = map_datasource_config_by_type(config)

    # read the datasource connections and return schemas
    db_schemas = read_datasources(ds_cfg_map)

    schema_str = "Datasources:\n"

    for db in db_schemas:
        schema_str += str(db) + "\n"

    return schema_str
