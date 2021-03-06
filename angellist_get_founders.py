"""
    Authors: Benjamin Hallen, Alex Murray, Siddharth Rao
    Date: 11/11/2015

    Fetches information about founders of startups in
    the United States of America given a startup name.
"""
import config
import requests
import json
import os
import sys
from pymongo import MongoClient
from bson.json_util import dumps
import time
reload(sys)
sys.setdefaultencoding('utf-8')

def fetch_id_of_startup_from_db(db, name_of_company):
    """
        @param name: The name of the company
        @return Returns the id of the startup from the database
        If the company is hidden, or name not found,
        returns None.
    """
    list_of_id = db.startups.distinct("id", {'lname':name_of_company})
    if len(list_of_id) > 0:
        return list_of_id[0]
    else:
        return None


def fetch_founders_for_startup(startup_id):
    """
        @params startup_id: The id of the startup
        @return  A list of dictionaries (json objects), each
        of which contains information about a founder of the startup

        Extra Info on the process:
            The AngelList API has one endpoint that
            returns all the founders* in a company. But that
            endpoint only returns basic information about
            the founders.

            Once we have access to the ids of the founders,
            we use another endpoint to fetch all the information
            about them.

            *Some founders are not correctly mentioned as founders.
            Still need to figure out what to do in that case.
                1 option:
                    Fetch all roles of that company.
    """
    params = {
        'access_token': config.CLIENT_TOKEN_AL,
        'v': 1,
        'startup_id': startup_id,
    }

    base_url = "https://api.angel.co/1/startup_roles"
    founder_info = requests.get(base_url, params)
    ids_of_CEOs = get_id_of_user(founder_info)
    #total_calls_to_api = total_calls_to_api + len(ids_of_CEOs)
    list_of_dictionaries = fetch_user_info_from_api(ids_of_CEOs, startup_id,                                                                False);

    base_url = "https://api.angel.co/1/startup_roles"
    params['role'] = 'founder'
    founder_info = requests.get(base_url, params)
    ids_of_CEOs = get_id_of_user(founder_info)
    #total_calls_to_api = total_calls_to_api + 2 + len(ids_of_CEOs)
    list_of_dictionaries.extend(fetch_user_info_from_api(ids_of_CEOs, startup_id,                                                                True))
    return list_of_dictionaries


def get_id_of_user(response):
    """
        @params
        response: The response text from startup_roles
        endpoint from AngelList's API
        isFounder: Boolean value representing if the
        employee is a founder or not. True if yes,
        false otherwise.

        @return Grabs the ids of the founders from the response
        and returns them as a list. If none found, returns
        an empty list
    """
    res = []
    if "startup_roles" in response.json().keys():
        for role in response.json()["startup_roles"]:
            res.append(role['tagged']['id'])
    return res


def fetch_user_info_from_api(list_of_ids, startup_id, isFounder):
    """
        @params
        list_of_ids: Contains the ids of founders in
        startup_id: The id of the startup. This id is added
        to the json object to quickly identify all founders
        of a company given the company id.

        @return
        A dictionary of json objects, each of which
        contains information about one founder.

    """
    result = []
    for user_id in list_of_ids:
        params = {
            'access_token': config.CLIENT_TOKEN_AL,
            'id': user_id
        }
        base_url = "https://api.angel.co/1/users/" + str(user_id)
        user_info = requests.get(base_url, params)
        json_dict = user_info.json()
        json_dict['startup_id'] = startup_id
        json_dict['isFounder'] = "true" if isFounder else "false"
        result.append(json_dict)
    return result



def save_founder_info_in_founders_db(list_of_dicts, db):
    """
        @params
        list_of_dicts: A list of dictionaries, each of which
        contains information for one founder of the company.
        db: A reference to the mongodb database

        PostCondition: For each of the founders in the list,
        saves their information to the database.
        If a document already exists in the database with the
        same founder name, updates it.
    """
    for founder in list_of_dicts:
        json_object = json.loads(dumps(founder))
        if not 'success' in json_object.keys():
            try:
                name_of_founder = json_object['name']
                key = {'name': name_of_founder}
                db.founders.update(key, json_object, True)
            except KeyError:
                print "Couldn't get this one."



def save_info_in_file(list_of_founders, name_of_company):
    """
        @params
        list_of_dicts: A list of dictionaries, each of which
        contains information for one founder of the company.
        name_of_company: The name of the company.

        PostCondition: Creates a folder for the company
        and saves the information of the founder in a json
        file in the folder.
        The file name would look like:
            <founder name>_<id on angellist>.json
        If there's already a file for that founder, updates it.
    """
    dirname = name_of_company
    if not os.path.isdir("founders/" + dirname):
        os.mkdir("founders/" + dirname)

    for founder in list_of_founders:
        if not 'success' in founder.keys():
            filename = founder['name'] + "_" + str(founder['id'])
            path = "founders/%s/%s.json" %(dirname, filename)
            outfile = open(path, 'w')
            json_object = json.loads(dumps(founder))
            json.dump(json_object, outfile, indent=2)


# if __name__ == '__main__':
#     client = MongoClient()
#     db = client['social-media-and-startups']
#     try:
#         name_of_company = sys.argv[1]
#         id_of_startup = fetch_id_of_startup_from_db(db, name_of_company)
#         # A list of founders/employees with each index a dictionary.
#         list_of_founders = fetch_founders_for_startup(id_of_startup)
#         if len(list_of_founders) > 0:
#             save_founder_info_in_founders_db(list_of_founders, db)
#             #save_info_in_file(list_of_founders, name_of_company)
#         else:
#             print "Couldn't find any founders :("
#
#     except IndexError:
#         print "Sorry, no arguments passed."
#         sys.exit(2)

if __name__ == '__main__':
    client = MongoClient()
    db = client['social-media-and-startups']
    list_of_names = sorted(db.startups.distinct("lname"))
    print list_of_names
    total_calls = 1581
    total_seconds = 1
    count = 0
    for name in list_of_names:
        count = count + 1
        if count % 10 == 0:
            print str(count) + "companies done."
        if total_seconds % 3300 == 0:
            print "Gonna sleep for 5 minutes"
            time.sleep(300)
            total_seconds = 0
        if  total_calls >= 1900:
            print "Gonna sleep for " + str(3600 - total_seconds)
            time.sleep(3600 - total_seconds)
            total_seconds = 0
        start_time = time.time()
        name_of_company = name
        id_of_startup = fetch_id_of_startup_from_db(db, name_of_company)
        # A list of founders/employees with each index a dictionary.
        list_of_founders = fetch_founders_for_startup(id_of_startup)
        total_calls = total_calls + len(list_of_founders)
        total_seconds = total_seconds + (time.time() - start_time)
        print "total calls: " + str(total_calls)
        print "total seconds: " + str(total_seconds)
        if len(list_of_founders) > 0:
            save_founder_info_in_founders_db(list_of_founders, db)
            #save_info_in_file(list_of_founders, name_of_company)
        else:
            print "Couldn't find any founders :("
