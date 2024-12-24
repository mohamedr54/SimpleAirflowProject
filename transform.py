import pandas as pd
import numpy as np
import json




def load_json_data_to_dict(filename):
    """
    this function takee the important data we stored and loads it in two files : one four hourly metrics and
    another one for daily metrics
    :param filename: name of the file we're going to extract data from
    :return: return a tuple composed of two dicts
    """
    with open(filename, "r") as file:  # extracting hourly and daily variables as proper dictionaries
        my_data = json.load(file)
    hourly_dict = my_data['hourly']
    daily_dict = my_data['daily']
    return hourly_dict, daily_dict



def dict_to_dataframe(hourly_dict, daily_dict):
    """
    this function transforms each dict into a pandas dataframe
    :param hourly_dict: hourly dict returned by load_json_data_to_dict function
    :param daily_dict: daily dict returned by load_json_data_to_dict function
    :return: return a tuple composed of two dataframes
    """
    hourly_df = pd.DataFrame.from_dict(hourly_dict)
    daily_df = pd.DataFrame.from_dict(daily_dict)
    return hourly_dict,daily_dict



def formating_time_columns(hourly_df, daily_df):
    """
    this function set the time column of each dataframe to a standard format. This will be necessary
    in order to merge the two dataframes.
    :param hourly_df: hourly dataframe returned by dict_to_dataframe function
    :param daily_df:  daily dataframe returned by dict_to_dataframe function
    :return: returns
    """
    hourly_df["time"] = pd.to_datetime(hourly_df["time"])
    daily_df["time"] = pd.to_datetime(daily_df["time"])
    return hourly_df, daily_df



def merging_both_dataframes(hourly_df, daily_df):
    """
    this function merges our both dataset into a final one, ordered by time

    note :  `merge_asof` is used to merge two DataFrames with different frequencies.
    The data must be sorted by the 'time' column before merging. This method matches each row
    from the `hourly_df` DataFrame to the row in the `daily_df` DataFrame with the closest
    'time' value, while preserving the chronological order.


    :param hourly_df: dataframe with hourly metrics and a proper time column
    :param daily_df: dataframe with daily metrics and a proper time column
    :return:
    """
    final_df = pd.merge_asof(hourly_df.sort_values('time'), daily_df.sort_values('time'))
    return final_df


def drop_duplicates(dataframe:pd.DataFrame):
    """
    this function drops duplicate rows
    :param dataframe:
    :return: returns a dataframe with duplicate rows dropped
    """
    dataframe.drop_duplicates(inplace=True)
    return dataframe



def dropping_nan_values(dataframe:pd.DataFrame):
    """
    this function deletes any row that contains NaN values

    NOTE : here I made the choice to delete rows with NaN values. I could have used cluster imputation method to fill
    some values in case or errors. However ,I need to pay attention to the context : weather is kind of unpredictable,
    so imputing data with a cluster could be meaningless. Moreover, since the data comes from a reliable website,
    I assume that very few rows should be impacted, and deleting them will not be a problem.
    :param dataframe: the dataframe we got by merging hourly and daily dataframes
    :return: returns a new dataframe without NaN values
    """
    dataframe.replace(np.nan, 0, inplace=True)
    return dataframe






def saving_to_csv(final_df):
    """
    this function saves the final dataframe to a csv file
    :param final_df: final dataframe
    """
    final_df.to_csv("final.csv")




