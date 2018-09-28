from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import seaborn as sns
import json

class TweetAnalyzer:

    def __init__(self, tweets=None):
        if not tweets:
            try:
                with open('flattened.json') as f:
                    self.tweets = json.load(f)
            except FileNotFoundError:
                print("Can't find the tweets file")
        else:
            self.tweets = tweets

        columns = ["screen_name", "text", "created_at", "retweet_count", "favorite_count", "favorited"]
        self.df = pd.DataFrame(self.tweets, columns=columns)
        print(self.df.head())

    def get_sentiments(self):

        fits = []
        for tweet in self.tweets:
            print(tweet)

ta = TweetAnalyzer()
# ta.get_sentiments()

