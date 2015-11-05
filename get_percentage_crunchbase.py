"""
    Authors: Benjamin Hallen, Alex Murray, Siddharth Rao

    Script to calculate the percentage
    of companies that have a crunchbase url
    The company information was retreived from
    Angel List API.
"""

from os import walk
import json

companies = []
# Walking through the companies.
for filenames in walk("./final_companies"):
    companies.extend(filenames)
    break

# Getting all the file names. The files exist in the second
# element.
companies = companies[2]

companies_error = []
sum = 0;
total_scanned = 0
for company in companies:
    total_scanned = total_scanned + 1
    if total_scanned % 1000 == 0:
        print total_scanned
    # Trying to access the json file.
    try :
        file_contents = open("./final_companies/%s" %(company)).read()
        json_text = json.loads(file_contents)
        if "crunchbase_url" in json_text:
            if not json_text["crunchbase_url"] == 'null':
                sum = sum + 1
    except ValueError:
        print "Couldn't count %s" %(company)
        companies_error.append(company)

# prints the total number of companies that have a crunchbase url
print "The num: " + str(sum);
# prints the companies that caused an error while accessing the json file.
print len(companies_error)
