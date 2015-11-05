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
reload(sys)
sys.setdefaultencoding('utf-8')

TOTAL_PAGES = 2500 # looked up from a sample request.

def fetch_companies(starting_point, end_point):
    """
        @params: starting_point: The starting page (inclusive)
                 end_point: The last page (not inclusive)

        Fetches companies given a starting page
        and an ending page.
    """
    url = "https://api.angel.co/1/tags/1688/startups"

    for page_number in range(starting_point, end_point):
        print "Fetching results for page %d ..." % (page_number)
        parameters = {
            "access_token": config.CLIENT_TOKEN_AL,
            "page": page_number
        }
        get_startups = requests.get(url, params = parameters)
        json_format = get_startups.json()
        save_data_in_json_files(json_format)


def save_data_in_json_files(json_format):
    """
        Saves data in JSON files for each of the startup
        Important Note:
            Some companies do not have a field for their name
            For those companies, stored in a file with ID as their name.
    """
    for startup in json_format["startups"]:
        if startup.has_key("id"):
            name = startup.get("name", startup["id"])
            if "/" in str(name):
                name = startup["id"] # to prevent the companies having "/" in names
            print "    Creating file for " + str(name) + " ..."
            destination = "final_companies/%s.json" %(name)
            outfile = open(destination, 'w')
            json.dump(startup, outfile)

# The first parameter included, the second one not.
# Example: fetch_companies(2, 10) would fetch pages
# 1 to 9
# Uncomment this line of code and provide the initial and the final page
# number.
#fetch_companies(0, 10)
