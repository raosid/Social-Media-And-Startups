"""
    Authors: Benjamin Hallen, Alex Murray, Siddharth Rao
    Date: 10/11/2015

    Fetches all tweets for startups companies and their CEOs.
"""

import config
import tweepy # http://tweepy.readthedocs.org/en/v3.4.0/
import csv # in order to read the csv file containing the list of accounts
import os # to create the directories for the companies.
import json

def get_tweets_for_csv_accounts():
    """
        Fetches all tweets (3240 is the twitter limit) for each of the
        companies and the CEO in the csv file and creates JSON files
        for each of the company.
    """
    file = open("list-of-startups.csv")
    csv_file = csv.reader(file)

    counter = 0
    for row in csv_file: # fetching the tweets
        dict_of_tweets = {}
        if counter > 0: # The first row contains the heading (Trash)

            if len(row[0]) > 0: # Checking if there is a company
                company_name = row[0]

                tweets_dictionary = {}
                tweets_dictionary["company"] = []
                tweets_dictionary["ceo"] = []

                # Getting the tweets for the company
                tweets_dictionary["company"] = get_tweets_for_handler(row[0], row[1])
                tweets_dictionary["ceo"] = get_tweets_for_handler(row[0], row[3])

                # Saving the tweets in a .json file
                save_tweets_to_file(tweets_dictionary, company_name)
        counter = counter + 1


def get_tweets_for_handler(company_name, handler):
    # Returns a list of tweets for the given handler.
    """
        @params: company_name: The name of the company whose tweets have to
                               be fetched.
                 handler: the twitter handler for the company's account or the
                          CEO's account
        @return: A list containing all the tweets from the handler.

        Note: Prints some helpful messages on the console to see the progress
              of the download.
    """
    list_of_tweets = []
    if len(handler) > 0:

        print "Fetching tweets for: " + company_name + "; " + handler

        # Fetch initial tweets in order to get the last id of the tweet
        timeline_object = api.user_timeline(handler, count = 200, wait_on_rate_limit = True,
                                            wait_on_rate_limit_notify = True) #limit is 200

        counter = 0
        for tweet in timeline_object:
            if counter == 0:
                list_of_tweets.append(tweet._json)


        # Get the id of the last tweet downloaded
        oldest_id = list_of_tweets[-1]["id"] - 1

        # Using that id to download tweets older than that id.
        while (len(timeline_object) > 0): # more tweets to fetch
            print "     Getting tweets after id " + str(oldest_id)

            # making another request for 200 tweets
            timeline_object = api.user_timeline(handler, count = 200, max_id = oldest_id, wait_on_rate_limit = True,
                                                wait_on_rate_limit_notify = True)

            for tweet in timeline_object:
                list_of_tweets.append(tweet._json)

            oldest_id = list_of_tweets[-1]["id"] - 1

            print "     Status: %s tweets downloaded." %(len(list_of_tweets))
    return list_of_tweets


def save_tweets_to_file(tweets_dictionary, company_name):
    """
        @params: tweets_dictionary: The dictionary containing all the tweets
                                    for a given company name.
                 company_name: The name of the company.

        Creates a directory for the company and creates two JSON files:
                1. Company's Tweets
                2. CEO's tweets
    """
    dirname = company_name
    if not os.path.isdir("tweets/" + dirname):
        os.mkdir("tweets/" + dirname)

    for account in tweets_dictionary:
        file_name = "tweets/" + company_name.lower() + "/%s.json" %(company_name.lower() + "_" + account)
        outfile = open(file_name, 'w')
        json.dump(tweets_dictionary[account], outfile)


# Initializing the state variables and setting up a connection
# to the API.
authentication = tweepy.OAuthHandler(config.API_KEY, config.API_SECRET)
authentication.set_access_token(config.ACCESS_TOKEN, config.ACCESS_SECRET)
api = tweepy.API(authentication)

get_tweets_for_csv_accounts()
