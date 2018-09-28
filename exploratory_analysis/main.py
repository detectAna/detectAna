from TwitterAuth import api
from functools import reduce
from UserCrawler import UserCrawler


# Instantiate a usercrawler
usercrawler = UserCrawler()

# get the users
usercrawler.get_users()

# get the tweets
usercrawler.get_user_tweets()
