import json
from functools import reduce
from TwitterAuth import api

DEBUG = True
class UserCrawler:

    def __init__(self, tweets_to_crawl_per_user=200):
        self.num_tweets_to_crawl = tweets_to_crawl_per_user
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

        ## TODO: CLEAN THE TWEETS HERE
        self.write_users_tofile('results_with_tweets.json')

        with open('flattened.json', 'w') as f:
            print("writing flattened")
            json.dump(flattened_tweets, f)

    def filter_users_by_keywords(self, user):
        description = user.description.lower()
        booleans = [keyword in description for keyword in self.recovery_keywords]
        return reduce(lambda x, y: x or y, booleans)

    def get_initial_users(self, read_from_file=False):

        # Read from results.json file
        if read_from_file:
            try:
                with open('results.json') as f:
                    self.tweets = json.load(f)
                    return self.tweets
            except FileNotFoundError:
                print("Can't find the tweets file")

        # Lambda function to filter the users based off of their descriptions
        # def filter_text(text):
        #     description = text['description'].lower()
        #     booleans = [keyword in description for keyword in self.recovery_keywords]
        #     return reduce(lambda x, y: x or y, booleans)

        possible_users = []

        # Don't scrape a user more than once
        scraped_usernames = set()
        for hashtag in self.hashtags:
            results = api.search(q="#{}".format(hashtag), count=100)
            for r in results:
                user = r.user
                if user.screen_name not in scraped_usernames:
                    scraped_usernames.add(user.screen_name)
                    possible_users.append(user)

        print("Found {} users BEFORE filtering".format(len(possible_users)))
        # Perform filtering based off of recovery_keywords
        filtered_users = list(filter(self.filter_users_by_keywords, possible_users))

        print("Found {} users AFTER filtering".format(len(filtered_users)))
        self.users = filtered_users
        self.write_users_tofile()
        return self.users

    # lower_threshold is the minimum amount of tweets that we want users to have
    # higher_threshold is the maximum amount of tweets that we want users to have
    # users is an array of users that is read from 'results.json'
    def crawl_from_existing_users(self, users, lower_threshold=1000, higher_threshold=30000):
        # Sort the users by the number of "statuses", or "tweets" DESCENDING
        sorted_users = sorted(users, key=lambda user: user.statuses_count, reverse=True)
        # Filter based off of the thresholdp
        sorted_users = list(filter(lambda user: user.statuses_count >= lower_threshold and user.statuses_count <= higher_threshold, sorted_users))
        print(len(sorted_users))
        for user in sorted_users:
            screen_name = user.screen_name
            followers_ids = api.followers_ids(screen_name=screen_name)
            following_ids = api.friends_ids(screen_name=screen_name)

            followers_count = len(followers_ids)
            following_count = len(following_ids)

            print(screen_name, followers_count, following_count)
            ## Filter out the followers and following
            # followers = list(filter(self.filter_users_by_keywords, followers))
            # following = list(filter(self.filter_users_by_keywords, following))

            # print("filtered out {} followers", followers_count - len(followers))
            # print("filtered out {} friends", following_count - len(following))

    def write_users_tofile(self, filename='results.json'):
        jsons = []
        for user in self.users:
            jsons.append(user._json)

        with open (filename, 'w') as f:
            json.dump(jsons, f)
