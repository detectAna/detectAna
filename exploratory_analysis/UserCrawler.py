import json
from functools import reduce
from TwitterAuth import api

DEBUG = True
USER_FILE = 'users.json'
TOTAL_REQUIRED_USERS = 100000


class UserCrawler:

    def __init__(self, tweets_to_crawl_per_user=200):
        self.num_tweets_to_crawl = tweets_to_crawl_per_user
        self.hashtags = [
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
        self.users = {'user_ids': set(), 'crawled': set(), 'total_users': 0}

    # new_users of datatype set
    def add_update_db(self, new_users):
        self.users['user_ids'].update(new_users)
        self.users['total_users'] += len(new_users)
        with open(USER_FILE, 'w') as user_file:
            write_obj = {
                'user_ids': list(self.users['user_ids']),
                'crawled': list(self.users['crawled']),
                'total_users': self.users['total_users']
            }
            json.dump(write_obj, user_file)

    def print_results(self):
        for user in self.users:
            print(user)

    def get_user_tweets(self):
        flattened_tweets = []
        for counter, user in enumerate(self.users):
            screen_name = user['screen_name']
            tweets = api.get_user_timeline(
                screen_name=screen_name, count=self.num_tweets_to_crawl, tweet_mode="extended")

            if DEBUG:
                print("Scraping last {} tweets for {}".format(
                    self.num_tweets_to_crawl, user['screen_name']))

            tweets = list(map(lambda tweet: {'screen_name': screen_name, 'text': tweet['full_text'], 'created_at': tweet['created_at'],
                                             'retweet_count': tweet['retweet_count'], 'favorite_count': tweet['favorite_count'], 'favorited': tweet['favorited']}, tweets))
            self.users[counter]['tweets'] = tweets
            print(tweet['full_text'])
            flattened_tweets.extend(tweets)

        return
        # TODO: CLEAN THE TWEETS HERE
        self.write_users_tofile('results_with_tweets.json')

        with open('flattened.json', 'w') as f:
            print("writing flattened")
            json.dump(flattened_tweets, f)

    def filter_users_by_keywords(self, user):
        if (type(user) is int):
            try:
                user = api.get_user(user)
            except:
                return False

        description = user.description.lower()
        booleans = [
            keyword in description for keyword in self.recovery_keywords]
        #print(user.screen_name, reduce(lambda x, y: x or y, booleans))
        return reduce(lambda x, y: x or y, booleans)

    def get_initial_users(self, read_from_file=False, lower_threshold=1000, higher_threshold=30000):

        # Read from results.json file
        if read_from_file:
            try:
                with open(USER_FILE) as user_file:
                    read_obj = json.load(user_file)
                    self.users['user_ids'] = set(read_obj['user_ids'])
                    self.users['crawled'] = set(read_obj['crawled'])
                    self.users['total_users'] = read_obj['total_users']
                    return self.users
            except FileNotFoundError:
                print("Can't find the tweets file")

        # Don't scrape a user more than once
        scraped_userids = set()
        for hashtag in self.hashtags:
            results = api.search(q="#{}".format(hashtag), count=500)
            for r in results:
                user = r.user
                scraped_userids.add(user.id)

        print("Found {} users BEFORE filtering".format(len(scraped_userids)))
        # Perform filtering based off of recovery_keywords
        filtered_users = set(
            filter(self.filter_users_by_keywords, scraped_userids))
        print("Found {} users AFTER filtering".format(len(filtered_users)))
        print(filtered_users)
        self.add_update_db(filtered_users)
        # self.write_users_tofile()
        return self.users

    # lower_threshold is the minimum amount of tweets that we want users to have
    # higher_threshold is the maximum amount of tweets that we want users to have
    # users is an array of users that is read from 'results.json'
    def crawl_from_existing_users(self, users, lower_threshold=1000, higher_threshold=30000, crawl_limit=TOTAL_REQUIRED_USERS):
        # Sort the users by the number of "statuses", or "tweets" DESCENDING
        #sorted_users = sorted(users, key=lambda user: user.statuses_count, reverse=True)
        # Filter based off of the thresholdp
        #sorted_users = list(filter(lambda user: user.statuses_count >= lower_threshold and user.statuses_count <= higher_threshold, sorted_users))
        # print(len(sorted_users))

        copy_set = users['user_ids'].copy()
        while True:
            for user_id in copy_set:
                if (users['total_users'] >= crawl_limit):
                    return
                if (user_id in users['crawled']):
                    continue

                followers_ids = api.followers_ids(id=user_id)
                following_ids = api.friends_ids(id=user_id)

                followers_count = len(followers_ids)
                following_count = len(following_ids)

                print('User : ', user_id, 'Followers : ',
                      followers_count, 'Following :', following_count)
                print('Before filtering followers : ', len(followers_ids))
                followers = set(
                    filter(self.filter_users_by_keywords, followers_ids))
                following = set(
                    filter(self.filter_users_by_keywords, following_ids))
                print('After filtering followers : ', len(followers))
                followers.update(following)
                users['crawled'].add(user_id)
                if len(followers) != 0:
                    self.add_update_db(followers)
            if (copy_set == users['user_ids']):
                print('no more change in set')
                break
            copy_set = users['user_ids'].copy()
            # Filter out the followers and following
            # followers = list(filter(self.filter_users_by_keywords, followers))
            # following = list(filter(self.filter_users_by_keywords, following))

            # print("filtered out {} followers", followers_count - len(followers))
            # print("filtered out {} friends", following_count - len(following))
