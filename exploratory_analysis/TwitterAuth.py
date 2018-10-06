# from twython import Twython
import tweepy

app_key = "GT3K2YSlEiLive1W20Uc3grNX"
app_sec = "Wi6e5IJ0KaAAUoOCLE1G2ICvvPJ53xc3ocAF1TBNxYh3TbsaxK"
user_key = "988796600746033152-X5EUzf6jHnFFwf8XncZ3Ti0fQBfHdA8"
user_sec = "a2vYkRKN6V7hXWVjN8upbD5TqU1ypZx2ejLPhdvjwTThA"

auth = tweepy.OAuthHandler(app_key, app_sec)
auth.set_access_token(user_key, user_sec)
api = tweepy.API(auth, retry_count = 3, retry_delay = 5, timeout=5, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# api = Twython(app_key, app_sec, user_key, user_sec)
# api.verify_credentials()
