import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#used so pytest can add parent directory in his research path, need to be set BEFORE the import from extract.py file7
import pytest
import json
from transform import *

def test_load_json_data_to_dict():

    filename="./tests/temp/testjson_to_load.txt"
    sample_to_write={"hourly": {"temperature_2m": [10, 12, 14]},
    "daily": {"temperature_2m_max": [15, 16, 17]}
    }
    with open(filename, "w") as file:
        json.dump(sample_to_write,file)

    test_hourly_dict, test_daily_dict = load_json_data_to_dict(filename)
    assert test_hourly_dict == {"temperature_2m": [10, 12, 14]}
    assert test_daily_dict == {"temperature_2m_max": [15, 16, 17]}



def test_example():
    assert 1 + 1 == 2
