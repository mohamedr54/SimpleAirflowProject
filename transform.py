import pandas as pd
import numpy as np
import json




def load_json_data_to_dict(filename:str):
    """
    this function take the important data we stored and loads it into a dictionary
    :param filename: name of the file we're going to extract data from
    :return: returns a dict
    """
    with open(filename, "r") as file:  # extracting hourly and daily variables as proper dictionaries
        my_data = json.load(file)
    my_dict = my_data['hourly']
    return my_dict



def dict_to_dataframe(my_dict:dict):
    """
    this function transforms each dict into a pandas dataframe
    :param my_dict:  dict returned by load_json_data_to_dict function
    :return: return a dataframe
    """
    my_df = pd.DataFrame.from_dict(my_dict)
    return my_df


def drop_duplicates(my_df:pd.DataFrame):
    """
    this function drops duplicate rows
    :param my_df: dataframe containing weather data
    :return: returns a dataframe with duplicate rows dropped
    """
    my_df.drop_duplicates(inplace=True)
    return my_df


def dropping_nan_values(my_df: pd.DataFrame) -> pd.DataFrame:
    """
    This function deletes any row that contains NaN values.

    NOTE: Here I made the choice to delete rows with NaN values. I could have used cluster imputation method to fill
    some values in case of errors. However, I need to pay attention to the context: weather is kind of unpredictable,
    so imputing data with a cluster could be meaningless. Moreover, since the data comes from a reliable website,
    I assume that very few rows should be impacted, and deleting them will not be a problem.

    :param my_df: The dataframe containing weather data
    :return: Returns a new dataframe without NaN values.
    """
    # Drop rows with any NaN values and reset the index
    return my_df.dropna().reset_index(drop=True)


def formating_time_column(my_df:pd.DataFrame ):
    """
    this function set the time column of each dataframe to a standard format. This will be necessary
    in order to merge the two dataframes.
    :param my_df: dataframe containing weather data
    :return: returns the dataframe with time column set to the right format
    """
    my_df["time"] = pd.to_datetime(my_df["time"])

    return my_df




def saving_to_csv(final_df : pd.DataFrame):
    """
    this function saves the final dataframe to a csv file
    :param final_df: clean dataframe
    """
    final_df.to_csv("final.csv")

