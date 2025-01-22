import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#used so pytest can add parent directory in his research path, need to be set BEFORE the import from extract.py file7
import pytest
import json
from unittest.mock import patch, mock_open
from extract import fetch_weather_data, extracting_useless_data, deleting_useless_data, saving_useful_data



def test_fetch_weather_data_success():
    url = "https://api.open-meteo.com/v1/forecast"
    parameters = {
        "latitude": 34.668138,
        "longitude": 104.16580199999999,
        "temperature_unit": "celsius",
        "wind_speed_unit": "kmh",
        "precipitation_unit": "mm",
        "hourly": ["temperature_2m","cloud_cover"]
    }

    mock_response = {
        "latitude": 34.625,
        "longitude": 104.125,
        "hourly": {"temperature_2m": [10, 12, 14],"cloud_cover": [0, 0, 3]}}
    #note :mocks are simulated objects which have the same behaviour as a real object

    # we use mock to simulate requests.get
    with patch("requests.get") as mock_get:#replace the fcn reguests.get by a simulated object
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        # here we call the function we want to test
        result = fetch_weather_data(url, parameters)

        # here we are checking if the function's behaviour is correct
        assert result == mock_response
        mock_get.assert_called_once_with(url,params=parameters)
        #note : checking that the function has correctly called


def test_fetch_weather_data_failure():

    url = "https://api.open-meteo.com/v1/forecast"
    parameters = {
        "latitude": 34.668138,
        "longitude": 104.16580199999999,
        "temperature_unit": "celsius",
        "wind_speed_unit": "kmh",
        "precipitation_unit": "mm",
        "hourly": ["temperature_2m","cloud_cover"]
    }

    # this time we simulate a server error
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 500

        # we expect an exception to be raised
        with pytest.raises(Exception):
            fetch_weather_data(url, parameters)


def test_extracting_useless_data():
    test = {
        "latitude": 34.625,
        "longitude": 104.125,
        "hourly": {"temperature_2m": [10, 12, 14],"cloud_cover": [0, 0, 3]},
    }

    liste = []
    filename = "./tests/temp/test_useless_data.txt"
    for element in test.keys():
        if element != "hourly":
            with open(filename, 'a') as file:
                string = element + " : " + str(test[element])
                file.write(string)
                file.write("\n")
                liste.append(element)

    with open(filename, "r") as f:
        my_content = f.read()
    assert my_content == "latitude : 34.625\nlongitude : 104.125\n"
    assert liste == ["latitude", "longitude"]
    os.remove(filename)


def test_deleting_useless_data():
    test_data = {
        "latitude": 34.625,
        "longitude": 104.125,
        "generationtime_ms": 0.0940561294555664,
        "utc_offset_seconds": 0,
        "timezone": "GMT",
        "hourly": {"temperature_2m": [10, 12, 14],"cloud_cover": [0, 0, 3]}
    }
    test_list_of_keys=[ "latitude","longitude","generationtime_ms","utc_offset_seconds","timezone",]
    assert deleting_useless_data(test_data,test_list_of_keys)== {"hourly": {"temperature_2m": [10, 12, 14],"cloud_cover": [0, 0, 3]}}


def test_saving_useful_data():
    # Initialisation (préparation des ressources)
    clean_fetched_data = {
        "hourly": {"temperature_2m": [10, 12, 14],"cloud_cover": [0, 0, 3]},
    }

    filename = "./tests/temp/test_clean_data.txt"
    saving_useful_data(clean_fetched_data,filename)

    with open (filename,"r") as f:
        expectations = json.load(f)

    assert saving_useful_data(clean_fetched_data, filename) == clean_fetched_data
    #écrire et assert que quand on ouvre le fichier on lise le bon truc

    os.remove(filename)