import json
from TwitterAPIManager import TwitterAPIPool

USER_INFO_DOWNLOAD_STATUS_FILE = 'user_info_download_status.json'
USER_TWEETS_DOWNLOAD_STATUS_FILE = 'user_tweets_download_status.json'
USER_INFO_FILE = 'user_metadata.jsonl'
USER_TWEET_FILE = 'user_tweets.jsonl'
DOWNLOAD_LIMIT = 10000

class UserDownloader():

    def __init__(self, user_ids, mode=None):
        self.users = user_ids
        self.mode = mode
        self.users_downloaded = { 'users_downloaded' : set(), 'total' : 0 }
        if (self.mode=='info'):
            self.api_pool = TwitterAPIPool('users', '/users/show/:id')
            self.USER_DOWNLOAD_STATUS_FILE = USER_INFO_DOWNLOAD_STATUS_FILE
        else :
            self.api_pool = TwitterAPIPool('statuses', '/statuses/user_timeline')
            self.USER_DOWNLOAD_STATUS_FILE = USER_TWEETS_DOWNLOAD_STATUS_FILE
        try:
            with open(self.USER_DOWNLOAD_STATUS_FILE, 'r') as user_download_file:
                read_obj = json.load(user_download_file)
                self.users_downloaded['users_downloaded'] = set(read_obj['users_downloaded'])
                self.users_downloaded['total'] = read_obj['total']
        except FileNotFoundError:
            print("Can't find the User Status file, downloading all")
            pass

    def add_user_status(self, user_id):
        self.users_downloaded['users_downloaded'].add(user_id)
        self.users_downloaded['total'] += 1
        with open(self.USER_DOWNLOAD_STATUS_FILE, 'w') as user_download_file :
            write_obj = {
            'users_downloaded' : list(self.users_downloaded['users_downloaded']),
            'total' : self.users_downloaded['total']
            }
            json.dump(write_obj, user_download_file)

    def save_user_info_downloaded(self, user_info):
        with open(USER_INFO_FILE, 'a') as user_info_file:
            user_info_file.write(json.dumps(user_info, default=str)+'\n')

    def save_user_tweets_downloaded(self, user_tweets):
        with open(USER_TWEET_FILE, 'a') as user_tweet_file:
            for each_tweet in user_tweets:
                user_tweet_file.write(json.dumps(each_tweet, default=str)+'\n')

    def extract_user_info(self,user_id, api):
        user = api.get_user(user_id)
        #return the meta data of user
        return list(
            map(
                lambda info: {
                'id' : info.id,
                'screen_name' : info.screen_name,
                'name' : info.name,
                'location' : info.location,
                'description' : info.description,
                'profile_location' : info.profile_location,
                'followers_count' : info.followers_count,
                'friends_count' : info.friends_count,
                'listed_count' : info.listed_count,
                'created_at' : info.created_at,
                'favourites_count' : info.favourites_count,
                'lang' : info.lang,
                'utc_offset' : info.utc_offset,
                'time_zone' : info.time_zone,
                'verified' : info.verified,
                'statuses_count' : info.statuses_count,
                } ,
                [user])
        )[0]

    def extract_tweets(self, user_id, api):
        #initialize a list to hold all the user Tweets
        alltweets = []
        #save the id of the oldest tweet less one
        oldest = None
        #keep grabbing tweets until there are no tweets left to grab
        while True:
            #all subsiquent requests use the max_id param to prevent duplicates
            new_tweets = api.user_timeline(id = user_id, count=200, max_id=oldest, tweet_mode="extended")
            if (len(new_tweets) == 0):
                break;

            #save most recent tweets
            alltweets.extend(new_tweets)
            #update the id of the oldest tweet less one
            oldest = alltweets[-1].id - 1
        #print(alltweets[0])
        return list(map(
            lambda tweet: {'id' : tweet.id,
                                       'text' :  tweet.full_text,
                                       'truncated' : tweet.truncated,
                                       'entities' : tweet.entities,
                                       'in_reply_to_status_id' : tweet.in_reply_to_status_id,
                                       'in_reply_to_user_id' : tweet.in_reply_to_user_id,
                                       'tweeter_id': tweet.user.id,
                                       'tweeter_screen_name' : tweet.user.screen_name } ,alltweets))

    def download_info(self, user_id):
        user_info = self.extract_user_info(user_id, self.api_pool.get_api())
        self.save_user_info_downloaded(user_info)
        return user_info

    def download_tweets(self, user_id):
        user_tweets = self.extract_tweets(user_id, self.api_pool.get_api())
        self.save_user_tweets_downloaded(user_tweets)
        return user_tweets

    def runner(self):

        for user_id in self.users:

            if user_id in self.users_downloaded['users_downloaded']:
                continue;

            if DOWNLOAD_LIMIT <= self.users_downloaded['total']:
                break

            if (self.mode=='info'):
                user = self.download_info(user_id)
                print('Downloaded user info ', user['screen_name'])
            else :
                user_tweets = self.download_tweets(user_id)
                print('Downloaded user ', user_id,' ', len(user_tweets) ,' tweets')
            self.add_user_status(user_id)
