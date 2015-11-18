"""
    Authors: Benjamin Hallen, Alex Murray, Siddharth Rao
    Date: 11/11/2015

    Fetches funding information about startups in
    the United States of America given a startup name.
"""

## NOTE: Just some testing code. Dabbling with the API.
# Can't find a good source to get the funding information.


import config
import requests
import json
import os
import sys
from pymongo import MongoClient
from bson.json_util import dumps
reload(sys)
sys.setdefaultencoding('utf-8')

params = {
    'access_token': config.CLIENT_TOKEN_AL,
    'filter': 'raising',
    'per_page': 2,
    'page': 1
}
base_url = "https://api.angel.co/1/startups/"
founder_info = requests.get(base_url, params)
print json.dumps(founder_info.json(), indent=2)
