"""
    Authors: Benjamin Hallen, Alex Murray, Siddharth Rao

    Stores the information for all companies in a
    MongoDB database.
"""
from pymongo import MongoClient
from os import walk
import json

client = MongoClient()
db = client['social-media-and-startups']

def add_startups_to_db():
    list_of_companies = get_all_companies()
    list_of_companies_not_added = []
    count = 0;
    for startup in list_of_companies:
        try :
            count = count + 1
            file_contents = open("./final_companies/%s" %(startup)).read()
            json_object = json.loads(file_contents)
            db.startups.insert_one(json_object)
            if count % 200 == 0:
                print count
        except ValueError:
            list_of_companies_not_added.append(startup)

    json_object_for_failures = json.loads(list_of_companies_not_added)
    db.failures.insert_one(json_object_for_failures)


def get_all_companies():
    companies = []
    for filenames in walk("./final_companies"):
        companies.extend(filenames)
        break
    return companies[2]

add_startups_to_db()
