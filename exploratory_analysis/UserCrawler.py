import json
from TwitterAuth import api


DEBUG = True
class UserCrawler:

    def __init__(self):
        try:
            with open('results.json') as f:
                self.users = json.load(f)
        except FileNotFoundError:
            print('results.json does not exist')
        self.num_tweets_to_crawl = 200


    def print_results(self):
        for user in self.users:
            print(user)

    def get_user_tweets(self):
        for user in self.users:
            tweets = api.get_user_timeline(screen_name=user['screen_name'], count=self.num_tweets_to_crawl)

            if DEBUG:
                print("Tweets for {}".format(user['screen_name']))
                print(tweets)

            user['tweets'] = tweets

        with open('reuslts_with_tweets.json', 'w') as f:
            print("Dumping data to file")
            json.dump(self.users, f)

usercrawler = UserCrawler()


usercrawler.get_user_tweets()
