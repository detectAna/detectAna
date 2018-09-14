import tweepy
import csv
import pandas as pd
####input your credentials here
consumer_key = "GT3K2YSlEiLive1W20Uc3grNX"
consumer_secret = "Wi6e5IJ0KaAAUoOCLE1G2ICvvPJ53xc3ocAF1TBNxYh3TbsaxK"
access_token = "988796600746033152-X5EUzf6jHnFFwf8XncZ3Ti0fQBfHdA8"
access_token_secret = "a2vYkRKN6V7hXWVjN8upbD5TqU1ypZx2ejLPhdvjwTThA"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)
#####United Airlines
# Open/Create a file to append data
csvFile = open('ua.csv', 'a')
#Use csv Writer
csvWriter = csv.writer(csvFile)

for tweet in tweepy.Cursor(api.search,q="#anorexia",count=100,
                           lang="en",
                           since="2018-09-01").items():
    print (tweet.created_at, tweet.text)
    csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])
