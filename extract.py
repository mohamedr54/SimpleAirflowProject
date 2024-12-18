import requests
import json



def fetch_weather_data(url: str,parameters: dict):
    """
    :param url: url of the API
    :param parameters: the list of variables we want to fetch
    :return: returns raw data from the weather website
    """
    fetched_data=requests.get(url,params=parameters)
    if fetched_data.status_code == 200:
        return fetched_data.json()
    else:
        raise Exception(f"Request failed with status code {fetched_data.status_code}")


def extracting_useless_data(fetched_data: dict,filename: str ="weather_info.txt"):
    """
    this function takes the information we do not want to store and save them in a txt file named weather_info.txt.
    We iterate through the dictionary, add each non-wanted element to the weather_info.txt file and save the key
    to remove the element later.
    :param filename: name of the file where useless information will be stored
    :param fetched_data: raw data fetched from weather website with fetch_weather_data function
    :return: returns a list of keys that must be deleted from the dictionary
    """
    keys_to_delete=[]
    for element in fetched_data.keys():
        if (element != "hourly") and (element != "daily"):
            with open(filename, 'a') as file:
                string = element + " : " + str(fetched_data[element])
                file.write(string)
                file.write("\n")
                keys_to_delete.append(element)
    return keys_to_delete

def deleting_useless_data(fetched_data: dict, list_of_keys: list):
    """
    remove elements that have been stored in the weather_info.txt file
    :param fetched_data: raw data fetched from weather website with fetch_weather_data function
    :param list_of_keys: the list of keys we obtained by using extracting_useless_data function
    :return:
    """
    for element in list_of_keys:
        del fetched_data[element]
    return fetched_data

def saving_useful_data(clean_fetched_data: dict,filename: str ="clean_data.json"):
    """

    :param filename: name of the file where clean data will be stored
    :param clean_fetched_data: the data fetched from web we want to store. it has been cleaned with
    deleting_useless_data function
    :return: it does not return anything.
    """
    with open(filename, "w") as f:
        json.dump(clean_fetched_data, f)











