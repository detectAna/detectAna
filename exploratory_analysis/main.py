from TwitterAuth import api
from functools import reduce
from UserCrawler import UserCrawler
from UserDownloader import UserDownloader
import sys

# Instantiate a usercrawler
usercrawler = UserCrawler()

# get the users
initial_users = usercrawler.get_initial_users(read_from_file=True)
#crawled_users = usercrawler.crawl_from_existing_users(initial_users)

user_downloader = UserDownloader(initial_users['user_ids'], sys.argv[1])
user_downloader.runner()
# get the tweets
# user_tweets = usercrawler.get_user_tweets()

# # Instantiate a tweet analyzer
# tweet_analyzer = TweetAnalyzer()
