import pandas as pd
import json
#penser à formatter le code avec black


def load_json_data_to_dict(filename):
    with open(filename, "r") as file:  # extracting hourly and daily variables as proper dictionaries
        data = json.load(file)
    hourly_dict = data['hourly']
    daily_dict = data['daily']
    return hourly, daily #returns a tuple


def json_to_dataframe(hourly_dict, daily_dict):
    hourly_df = pd.DataFrame.from_dict(hourly_dict)
    daily_df = pd.DataFrame.from_dict(daily_dict)
    return hourly_dict,daily_dict


def formating_time_columns(hourly_df, daily_df):
    hourly_df["time"] = pd.to_datetime(hourly_df["time"])
    daily_df["time"] = pd.to_datetime(daily_df["time"])
    return hourly_df, daily_df


def merging_both_dataframes(hourly_df, daily_df):
    final_df = pd.merge_asof(hourly_df.sort_values('time'), daily_df.sort_values('time'))
    """
    note :  `merge_asof` is used to merge two DataFrames with different frequencies.
    The data must be sorted by the 'time' column before merging. This method matches each row 
    from the `hourly_df` DataFrame to the row in the `daily_df` DataFrame with the closest 
    'time' value, while preserving the chronological order.
    """
    return final_df

def saving_to_csv(final_df):
    final_df.to_csv("final.csv")
    return None



with open("data.json", "r") as file:  # extracting hourly and daily variables as proper dictionaries
    data = json.load(file)
hourly = data['hourly']
daily = data['daily']



