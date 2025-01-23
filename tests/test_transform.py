import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#used so pytest can add parent directory in his research path, need to be set BEFORE the import from extract.py file7
import pytest
import json
from transform import *


def test_load_json_data_to_dict():

    filename="./tests/temp/testjson_to_load.txt"
    sample_to_write={"hourly": {"temperature_2m": [10, 12, 14],
                                "cloud_cover": [0, 0, 3]},
    }

    with open(filename, "w") as file:
        json.dump(sample_to_write,file)

    my_dict = load_json_data_to_dict(filename)
    assert my_dict == {"temperature_2m": [10, 12, 14],
                       "cloud_cover": [0, 0, 3]}



def test_dict_to_dataframe():
    test_my_dict = {"temperature_2m": [10, 12, 14],
                    "cloud_cover": [0, 0, 3]}
    test_my_df = dict_to_dataframe(test_my_dict)

    expected_df=pd.DataFrame(test_my_dict)
    pd.testing.assert_frame_equal(test_my_df, expected_df)


def test_drop_duplicates():

    test_df = df = pd.DataFrame({
    "time": [
        pd.Timestamp("2024-12-17 00:00:00"), pd.Timestamp("2024-12-17 01:00:00"),
        pd.Timestamp("2024-12-17 02:00:00"), pd.Timestamp("2024-12-17 03:00:00"),
        pd.Timestamp("2024-12-17 00:00:00"), pd.Timestamp("2024-12-17 02:00:00")],
    "temperature": [12, 15, 18, 20, 12, 18],
    "cloud_cover": [0, 0, 3, 4, 0, 3]
})


    drop_duplicates(test_df)

    expected_df = pd.DataFrame({
            "time": [pd.Timestamp("2024-12-17 00:00:00"), pd.Timestamp("2024-12-17 01:00:00"),
                     pd.Timestamp("2024-12-17 02:00:00"), pd.Timestamp("2024-12-17 03:00:00")],
            "temperature": [12, 15, 18,20],"cloud_cover": [0, 0, 3,4]})

    pd.testing.assert_frame_equal(test_df, expected_df)


def dropping_nan_values(my_df: pd.DataFrame) -> pd.DataFrame:
    """
    This function deletes any row that contains NaN values.

    NOTE: Here I made the choice to delete rows with NaN values. I could have used cluster imputation method to fill
    some values in case of errors. However, I need to pay attention to the context: weather is kind of unpredictable,
    so imputing data with a cluster could be meaningless. Moreover, since the data comes from a reliable website,
    I assume that very few rows should be impacted, and deleting them will not be a problem.

    :param my_df: The dataframe we got by merging hourly and daily dataframes.
    :return: Returns a new dataframe without NaN values.
    """
    return my_df.dropna().reset_index(drop=True)

def test_dropping_nan_values():
    test_df = pd.DataFrame({
        "time": [
            pd.Timestamp("2024-12-17 00:00:00"), pd.Timestamp("2024-12-17 01:00:00"),
            pd.Timestamp("2024-12-17 02:00:00"), pd.Timestamp("2024-12-17 03:00:00"),
            pd.NaT],
        "temperature": [12, 15, None, 20, None],
        "cloud_cover": [0, 0, 3, 4, 5]
    })

    result_df = dropping_nan_values(test_df)

    expected_df = pd.DataFrame({
        "time": [pd.Timestamp("2024-12-17 00:00:00"), pd.Timestamp("2024-12-17 01:00:00"),
                 pd.Timestamp("2024-12-17 03:00:00")],
         "temperature": [12.0, 15.0, 20.0], #droping nan values make the column type becoming float
        "cloud_cover": [0, 0, 4]
    })

    result_df = dropping_nan_values(test_df)

    pd.testing.assert_frame_equal(result_df, expected_df)



def test_formating_time_columns():

        test_df = pd.DataFrame({
            "time": ["2024-12-17T00:00", "2024-12-17T01:00", "2024-12-17T02:00", "2024-12-17T03:00"],
            "temperature": [12, 15, 18,20],
            "cloud_cover": [0, 0, 3,4]
        })

        formating_time_column(test_df)

        expected_df = pd.DataFrame({
            "time": [pd.Timestamp("2024-12-17 00:00:00"), pd.Timestamp("2024-12-17 01:00:00"),
                     pd.Timestamp("2024-12-17 02:00:00"), pd.Timestamp("2024-12-17 03:00:00")],
            "temperature": [12, 15, 18,20],
            "cloud_cover": [0, 0, 3,4]})


        assert test_df["time"].equals(expected_df["time"])



def test_saving_to_csv(tmp_path):
    data = pd.DataFrame({
        "time": [pd.Timestamp("2024-12-17 00:00:00"), pd.Timestamp("2024-12-17 01:00:00")],
        "temperature": [12, 15],
        "cloud_cover": [0, 0]
    })

    csv_path = "./tests/temp/final.csv"

    data.to_csv(csv_path, index=False) #removes the index when saving the file

    saved_df = pd.read_csv(csv_path)

    saved_df['time'] = pd.to_datetime(saved_df['time'])#needed because when we load the csv, date is at a str format

    pd.testing.assert_frame_equal(data, saved_df)

