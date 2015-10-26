"""
    Authors: Benjamin Hallen, Alex Murray, Siddharth Rao
    Date: 10/11/2015

    Fetches tweets for companies and their CEOs.

    Initially the tweets are stored in .txt files (Just testing some stuff.)
    Note: Only fetches 200 tweets per user. Decreased the limit for testing
          purposes. Limit can be increased with some tweaking to the code.
"""

import config
import tweepy # http://tweepy.readthedocs.org/en/v3.4.0/
import csv # in order to read the csv file containing the list of accounts
import os
import json

def get_tweets_for_csv_accounts():
    # Fetches 200 tweets for each user in the csv file and
    # stores them in a text file named after the company.
    file = open("list-of-startups.csv")
    csv_file = csv.reader(file)

    counter = 0
    for row in csv_file: # fetching the tweets
        dict_of_tweets = {}
        if counter > 1 and counter < 3: # The first row contains the heading (Trash/Throwaway)

            if len(row[0]) > 0: # Checking if there is a company
                # Creating a directory for the company.
                company_name = row[0]

                tweets_dictionary = {}
                tweets_dictionary["company"] = []
                tweets_dictionary["ceo"] = []

                # Getting the tweets for the company
                tweets_dictionary["company"] = get_tweets_for_handler(row[0], row[1])
                tweets_dictionary["ceo"] = get_tweets_for_handler(row[0], row[3])
                save_tweets_to_file(tweets_dictionary, company_name)
        counter = counter + 1

        # Saving the tweets in a text file.



def get_tweets_for_handler(company_name, handler):
    # Returns a list of tweets for the given handler.
    if len(handler) > 0:

        print "Fetching tweets for: " + company_name + "; " + handler

        timeline_object = api.user_timeline(handler, count = 200) #limit is 200
        list_of_tweets = []
        counter = 0
        for tweet in timeline_object:
            if counter == 0:
                list_of_tweets.append(tweet._json)


        oldest_id = list_of_tweets[-1]["id"] - 1 # to remember the last tweet grabbed
        # fetching the rest of the tweets
        while (len(timeline_object) > 0): # more tweets to fetch
            print "     Getting tweets after id " + str(oldest_id)

            # making another request for 200 tweets
            timeline_object = api.user_timeline(handler, count = 200, max_id = oldest_id)

            for tweet in timeline_object:
                list_of_tweets.append(tweet._json)

            oldest_id = list_of_tweets[-1]["id"] - 1

            print "     Status: %s tweets downloaded." %(len(list_of_tweets))



    return list_of_tweets


def save_tweets_to_file(tweets_dictionary, company_name):
    # Creates a text file and saves the 200 tweets from
    # the list passed in the text file.
    # params: api: The connection to the API
    #         list_tweets: The list of tweets
    file_name = "tweets/%s.json" %(company_name.lower())
    outfile = open(file_name, 'w')
    json.dump(tweets_dictionary, outfile)


# Initializing the state variables and setting up a connection
# to the API.
authentication = tweepy.OAuthHandler(config.API_KEY, config.API_SECRET)
authentication.set_access_token(config.ACCESS_TOKEN, config.ACCESS_SECRET)
api = tweepy.API(authentication)

get_tweets_for_csv_accounts()
