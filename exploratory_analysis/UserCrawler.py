import json
from functools import reduce
from TwitterAuth import api

DEBUG = True
class UserCrawler:

    def __init__(self):
        self.num_tweets_to_crawl = 200
        self.hashtags =[
            'eatingdisorder',
            'eatingdisorders',
            'edproblems',
            'edrecovery',
            'edlogic',
            'anorexia',
            'thinspo',
            'anarecovery',
        ]

        # Recovery keywords
        self.recovery_keywords = [
            'recovery',
            'recovered',
            'survivor',
            'advocate'
        ]

    def print_results(self):
        for user in self.users:
            print(user)

    def get_user_tweets(self):
        flattened_tweets = []
        for counter, user in enumerate(self.users):
            screen_name = user['screen_name']
            tweets = api.get_user_timeline(screen_name=screen_name, count=self.num_tweets_to_crawl)

            if DEBUG:
                print("Scraping last {} tweets for {}".format(self.num_tweets_to_crawl, user['screen_name']))

            tweets = list(map(lambda tweet: {'screen_name': screen_name, 'text': tweet['text'], 'created_at': tweet['created_at'], 'retweet_count': tweet['retweet_count'], 'favorite_count': tweet['favorite_count'], 'favorited': tweet['favorited']}, tweets))
            self.users[counter]['tweets'] = tweets

            flattened_tweets.extend(tweets)
        self.write_users_tofile('results_with_tweets.json')

        with open('flattened.json', 'w') as f:
            print("writing flattened")
            json.dump(flattened_tweets, f)


    def get_users(self):

        # function to filter the users based off of their descriptions
        def filter_text(text):
            description = text['description'].lower()
            booleans = [keyword in description for keyword in self.recovery_keywords]
            return reduce(lambda x, y: x or y, booleans)

        possible_users = []

        # Don't scrape a user more than once
        scraped_usernames = set()
        for hashtag in self.hashtags:
            results = api.search(q="#{}".format(hashtag), count=100).get('statuses')

            for r in results:
                user = r['user']
                if user['screen_name'] not in scraped_usernames:
                    scraped_usernames.add(user['screen_name'])
                    possible_users.append(user)
        print("Found {} users BEFORE filtering".format(len(possible_users)))
        # Perform filtering based off of recovery_keywords
        filtered_users = list(filter(filter_text, possible_users))

        print("Found {} users AFTER filtering".format(len(filtered_users)))
        self.users = filtered_users
        self.write_users_tofile()
        return self.users

    def write_users_tofile(self, filename='results.json'):
        with open (filename, 'w') as f:
            json.dump(self.users, f)
