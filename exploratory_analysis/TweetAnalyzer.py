from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
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

    def plot(self):
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_result = vectorizer.fit_transform(self.df['text'])

        scores = zip(vectorizer.get_feature_names(),
        np.asarray(tfidf_result.sum(axis=0)).ravel())

        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)

        labels, scores = [], []
        for item in sorted_scores[:100]:
            print("{0:50} Score: {1}".format(item[0], item[1]))
            # sns.distplot(item[1], label=item[0])
            labels.append(item[0])
            scores.append(item[1])

        y_pos = np.arange(len(scores))

        plt.bar(np.arange(max(scores)), scores, color="blue")
        plt.xticks(y_pos, labels)
        plt.show()



ta = TweetAnalyzer()
ta.plot()
# ta.get_sentiments()

