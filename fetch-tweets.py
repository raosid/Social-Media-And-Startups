"""
    Author: Siddharth Rao
    Date: 10/11/2015

    Fetches public tweets from certain users.
"""

import config
import tweepy #http://tweepy.readthedocs.org/en/v3.4.0/

# Testing out some basic code out for a single user.
authentication = tweepy.OAuthHandler(config.API_KEY, config.API_SECRET)
api = tweepy.API(authentication)

gustoHQ = api.get_user("GustoHQ")
print gustoHQ.followers_count
