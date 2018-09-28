from twython import Twython

app_key = "GT3K2YSlEiLive1W20Uc3grNX"
app_sec = "Wi6e5IJ0KaAAUoOCLE1G2ICvvPJ53xc3ocAF1TBNxYh3TbsaxK"
user_key = "988796600746033152-X5EUzf6jHnFFwf8XncZ3Ti0fQBfHdA8"
user_sec = "a2vYkRKN6V7hXWVjN8upbD5TqU1ypZx2ejLPhdvjwTThA"

api = Twython(app_key, app_sec, user_key, user_sec)
api.verify_credentials()
