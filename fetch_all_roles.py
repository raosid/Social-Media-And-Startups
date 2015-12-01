"""
    Authors: Benjamin Hallen, Alex Murray, Siddharth Rao
    Date: 11/11/2015

    Fetches all roles within each of the startups
    in the United States. Stores all information
    in a database.
"""
import os
import pymongo
import angellist_get_founders
from pymongo import MongoClient

def get_all_startup_ids():
    client = MongoClient()
    db = client['social-media-and-startups']
    list_of_startup_ids = db.startups.distinct("lname")
    total_seconds = 0
    for name in list_of_startup_ids:
        name_of_command = "python angellist_get_founders.py " + name
        os.system(name_of_command)
        print "downloading information for " + name

get_all_startup_ids()
