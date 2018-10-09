import json
from TwitterAPIManager import TwitterAPIPool

USER_DOWNLOAD_STATUS_FILE = 'user_download_status.json'
USER_INFO_FILE = 'user_metadata.jsonl'
USER_TWEET_FILE = 'user_tweets.jsonl'

class UserDownloader():

    def __init__(self, user_ids):
        self.users = user_ids
        self.users_downloaded = { 'users_downloaded' : set(), 'total' : 0 }
        try:
            with open(USER_DOWNLOAD_STATUS_FILE, 'r') as user_download_file:
                read_obj = json.load(user_download_file)
                self.users_downloaded['users_downloaded'] = set(read_obj['users_downloaded'])
                self.users_downloaded['total'] = read_obj['total']
        except FileNotFoundError:
            print("Can't find the User Status file, downloading all")
            pass

    def add_user_status(self, user_id):
        self.users_downloaded['users_downloaded'].add(user_id)
        self.users_downloaded['total'] += 1
        with open(USER_DOWNLOAD_STATUS_FILE, 'w') as user_download_file :
            write_obj = {
            'users_downloaded' : list(self.users_downloaded['users_downloaded']),
            'total' : self.users_downloaded['total']
            }
            json.dump(write_obj, user_download_file)

    def save_user_downloaded(self, user_info, user_tweets):

        with open(USER_INFO_FILE, 'a') as user_info_file:
            user_info_file.write(json.dumps(user_info))

        with open(USER_TWEET_FILE, 'a') as user_tweet_file:
            for each_tweet in user_tweets:
                user_tweet_file.write(json.dumps(each_tweet))

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
                'verified' : info.verified} ,
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

            if (len(new_tweets) == 0) :
                break;

    		#save most recent tweets
    		alltweets.extend(new_tweets)

    		#update the id of the oldest tweet less one
    		oldest = alltweets[-1].id - 1

        return list(
            map(
                lambda tweet: {
                'id' : info.id,
                'screen_name' : info.screen_name,
                'name' : info.name} ,
                alltweets)
        )

    def runner():

        for user_id in user_ids:

            if user_id in self.users_downloaded['users_downloaded']:
                continue;

            user_info = self.extract_user_info(user_id, api)

            user_tweets = self.extract_tweets(user_id, api)

            self.save_user_downloaded(user_info, user_tweets)
            self.add_user_status(user_id)
