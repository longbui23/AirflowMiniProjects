import io
import pandas as pd
import requests
from mage_ai.data_preparation.decorators import data_loader, typing_extensions

@data_loader
def load_data_from_api(*args, **kwargs):
    import pandas as pd

    url = '../data/uber_data.csv'

    return pd.read_csv('io.StringIO(response.text)',sep=',')

@test
def test_output(output, *args):
    assert output is None, 'The output is undefined'
