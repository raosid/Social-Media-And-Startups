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

def get_tweets_for_csv_accounts(api):
    # Fetches 200 tweets for each user in the csv file and
    # stores them in a text file named after the company.
    file = open("list-of-startups.csv")
    csv_file = csv.reader(file)

    counter = 0
    dict_of_tweets = {}
    for row in csv_file: # fetching the tweets
        if counter > 1 and counter < 3: # The first row contains the heading (Trash/Throwaway)
            get_tweets_for_handler(row[0], row[1], api, dict_of_tweets) #1 is column of twitter handle
        counter = counter + 1

    # Saving the tweets in a text file.
    # save_tweets_to_text_files(dict_of_tweets)


def get_tweets_for_handler(company_name, handler, api, dict_of_tweets):
    # Returns a list of tweets for the given handler.
    if len(handler) > 0:
        timeline_object = api.user_timeline(handler, count = 200) #limit is 200

        list_of_tweets = []
        for tweet in timeline_object:
            if tweet.id == 657614137376137216:
                list_of_tweets.append(tweet)
                dict_of_tweets[company_name] = list_of_tweets




def save_tweets_to_text_files(dict_of_tweets):
    # Creates a text file and saves the 200 tweets from
    # the list passed in the text file.
    # params: api: The connection to the API
    #         list_tweets: The list of tweets

    for company in dict_of_tweets:
        complete_name = os.path.abspath("initial-tweets/%s.txt" % company)
        f = open(complete_name, 'w')
        counter = 1
        for tweet in dict_of_tweets[company]:
            f.write(str(counter) + ". " + tweet)
            f.write("\n") #adding a blank line for every tweet
            counter = counter + 1

if __name__ == '__main__':
    # Initializing the state variables and setting up a connection
    # to the API.
    authentication = tweepy.OAuthHandler(config.API_KEY, config.API_SECRET)
    authentication.set_access_token(config.ACCESS_TOKEN, config.ACCESS_SECRET)
    api = tweepy.API(authentication)

    get_tweets_for_csv_accounts(api)
