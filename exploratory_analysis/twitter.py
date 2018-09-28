from twython import TwythonStreamer, Twython
from functools import reduce
import json

# Load in OAuth Tokens
app_key = "GT3K2YSlEiLive1W20Uc3grNX"
app_sec = "Wi6e5IJ0KaAAUoOCLE1G2ICvvPJ53xc3ocAF1TBNxYh3TbsaxK"
user_key = "988796600746033152-X5EUzf6jHnFFwf8XncZ3Ti0fQBfHdA8"
user_sec = "a2vYkRKN6V7hXWVjN8upbD5TqU1ypZx2ejLPhdvjwTThA"

api = Twython(app_key, app_sec, user_key, user_sec)
api.verify_credentials()

verified_users = [
    'ughliest',
    'byebyeanorexia',
    'Lily_Qi',
    'lmlosingmyself',
    'lisabethkaeser',
    'hannahxxashley',
    'omfgitstabitha',
    'Skinnyorexic',
    'Thintoxicating',
    'BrazenlyRy',
    'nowimawarrior24'
]

hashtags =[
    'eatingdisorder',
    'eatingdisorders',
    'edtwitter',
    'edproblems',
    'edrecovery',
    'edlogic',
    'anorexia'
]

# Recovery keywords
recovery_keywords = [
    'recovery',
    'recovered',
    'survivor',
    'advocate'
]


def filter_text(text):
    description = text['description'].lower()
    booleans = [keyword in description for keyword in recovery_keywords]
    return reduce(lambda x, y: x or y, booleans)


def get_possible_users():
    possible_users = []

    for hashtag in hashtags:
        results = api.search(q="#{}".format(hashtag)).get('statuses')
        possible_users.extend([r['user'] for r in results])

    filtered_users = list(filter(filter_text, possible_users))
    print("Found {} users".format(len(filtered_users)))
    with open ('results.json', 'w') as f:
        json.dump(filtered_users, f)

get_possible_users()
