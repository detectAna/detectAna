from heapq import heappush, heappop, heapify
import tweepy
import json

KEY_FILE = "keys.json"

class API :

    def __init__(self, key):
        auth = tweepy.OAuthHandler(key["app_key"], key["app_sec"])
        auth.set_access_token(key["user_key"], key["user_sec"])
        self.api = tweepy.API(auth, retry_count = 3, retry_delay = 5*60, timeout=15*60, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        self.name = key["name"]

class TwitterAPIPool:

    def __init__(self, category, sub_category):
        self.app_creds = []
        self.category = category
        self.sub_category = sub_category
        with open(KEY_FILE, 'r') as key_file:
            keys = json.load(key_file)
            for i, key in enumerate(keys['keys']) :
                app = API(key)
                self.add_app_key(i, app)

    def add_app_key(self, pos ,app):
        rate_limit_status = app.api.rate_limit_status()['resources'][self.category][self.sub_category]
        priority_remaining_requests = -1* rate_limit_status['remaining']
        priority_reset_time = rate_limit_status['reset']
        #print(app.name, pos, priority_remaining_requests, priority_reset_time)
        heappush(self.app_creds, (priority_remaining_requests, priority_reset_time , pos, app))

    def get_api(self):
        heapify(self.app_creds)
        app_min_wait_ = heappop(self.app_creds)
        pos = app_min_wait_[2]
        app = app_min_wait_[3]
        self.add_app_key(pos, app)
        return app.api

    def __len__(self):
        return len(self.app_creds)

    def __iter__(self):
        return self

    def next(self):
        try :
            return self.get_api()
        except IndexError:
            raise StopIteration
