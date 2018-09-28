from TwitterAuth import api
from functools import reduce
from UserCrawler import UserCrawler
from TweetAnalyzer import TweetAnalyzer


# Instantiate a usercrawler
usercrawler = UserCrawler()

# get the users
usercrawler.get_users()

# get the tweets
user_tweets = usercrawler.get_user_tweets()

# Instantiate a tweet analyzer
tweet_analyzer = TweetAnalyzer()
