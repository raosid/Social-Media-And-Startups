"""
    Authors: Benjamin Hallen, Alex Murray, Siddharth Rao
    Date: 10/24/2015

    Fetches information about startups in the United States.
"""
import config
import requests
import json
import os
import sys
from pymongo import MongoClient
reload(sys)
sys.setdefaultencoding('utf-8')


def fetch_id_of_startups_from_db(db):
    """
        Returns a list of ids of startups in the US.
    """
    return db.startups.distinct("id", {'hidden': False})


def fetch_founders_for_startup(startup_id):
    """

    """
    params = {
        'access_token': config.CLIENT_TOKEN_AL,
        'v': 1,
        'startup_id': startup_id # Test case for Angel List
    }
    base_url = "https://api.angel.co/1/startup_roles"
    founder_info = requests.get(base_url, params)
    ids_of_CEOs = get_id_of_user(founder_info)
    list_of_dictionaries = fetch_user_info_from_api(ids_of_CEOs, startup_id)

    return list_of_dictionaries


def get_id_of_user(response):
    res = []
    if "startup_roles" in response.json().keys():
        for role in response.json()["startup_roles"]:
            res.append(role['tagged']['id'])
    return res


def fetch_user_info_from_api(list_of_ids, startup_id):
    # returns a list of dictionaries (each containing)
    # information about a founder
    result = []
    for user_id in list_of_ids:
        params = {
            'access_token': config.CLIENT_TOKEN_AL,
            # 'id': user_id
        }
        base_url = "https://api.angel.co/1/users/" + str(user_id)
        user_info = requests.get(base_url, params)
        json_dict = user_info.json()
        json_dict['startup_id'] = startup_id
        result.append(json_dict)
    return result



def save_founder_info_in_founders_db(list_of_dicts, db):
    for dictionary in list_of_dicts:
        db.founders.insert_one(dictionary)


if __name__ == '__main__':
    client = MongoClient()
    db = client['social-media-and-startups']
    list_of_startup_ids = fetch_id_of_startups_from_db(db)
    counter = 0
    for startup_id in list_of_startup_ids:
        counter = counter + 1
        list_of_founders = fetch_founders_for_startup(startup_id)
        save_founder_info_in_founders_db(list_of_founders, db)
        if counter % 20 == 0:
            print "counter = " + str(counter)
