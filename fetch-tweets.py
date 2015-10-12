"""
    Authors: Benjamin Hallen, Alex Murray, Siddharth Rao
    Date: 10/11/2015

    Fetches public tweets from certain users. Retrieves
    of those users stored in a csv file.

    Initially the tweets are stored in .txt files (Just testing some stuff.)

    Note: Only fetches 200 tweets per user. Decreased the limit for testing
          purposes. Limit can be increased.
"""

import config
import tweepy # http://tweepy.readthedocs.org/en/v3.4.0/
import csv # in order to read the csv file containing the list of accounts

# Testing out some basic code out for a single user.
def get_tweets_for_csv_accounts(api):
    # Fetches 200 tweets for each user in the csv file and
    # stores them in a text file named after the company.
    file = open("list-of-startups.csv")
    csv_file = csv.reader(file)

    counter = 0
    for row in csv_file: # fetching the tweets
        if counter > 0: # The first row contains the heading (Trash/Throwaway)
            tweets = get_tweets_for_handler(row[1], api) #1 is column of twitter handle
    # saving the tweets in a text file
    


def get_tweets_for_handler(handler, api):
    # Returns a list of tweets for the given handler. Limits the number
    # of tweets to 200.
    if len(handler) > 0:
        timeline_object = api.user_timeline(handler, count = 200) #limit is 200
        list_of_tweets = list()
        for tweet in timeline_object:
            list_of_tweets.append(tweet.text)
        return list_of_tweets
    return []


if __name__ == '__main__':
    # Initializing the state variables and setting up a connection
    # to the API.
    authentication = tweepy.OAuthHandler(config.API_KEY, config.API_SECRET)
    authentication.set_access_token(config.ACCESS_TOKEN, config.ACCESS_SECRET)
    api = tweepy.API(authentication)

    get_tweets_for_csv_accounts(api)
