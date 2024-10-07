from mage_ai.data_preparation.repo_manager import get_repo_path
from mage_ai.io.bigquery import BigQuery
from mage_ai.io.config import ConfigFileLoader
from pandas import DataFrame
from os import path
from mage_ai.data_preparation.decorators import data_exporter

def export_data_to_big_query(data, **kwargs):
    config_path = path.join(get_repo_path(),'io_config_yaml')
    config_profile = 'default'

    for key, value in data.items():
        table_id = 'data-with-darshill.uber_data_engineering_yt.{}'.format(key)
        BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).export(
            DataFrame(value),
            table_id,
            if_exists='replace', 
        )
