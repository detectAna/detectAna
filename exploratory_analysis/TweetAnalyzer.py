from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import json
import jsonlines
from TweetCleaner import TweetCleaner
from timeit import default_timer as timer

TWEETS_FILE = 'user_tweets.jsonl'
DEBUG = True


class TweetAnalyzer:

    def __init__(self, tweets=None):
        if not tweets:
            try:
                with jsonlines.open(TWEETS_FILE) as reader:
                    self.tweets = [tweet for tweet in reader]
                    print('Loaded {} tweets fron {}'.format(
                        len(self.tweets), TWEETS_FILE))
            except FileNotFoundError:
                print("Can't find the tweets file")
            except Exception as e:
                print(e)
        else:
            self.tweets = tweets
        # Extract the keys from the first tweet and spread them into a list
        columns = [*self.tweets[0]]
        self.df = pd.DataFrame(self.tweets, columns=columns)
        self.clean_tweets()
        if DEBUG:
            print(self.df.head())

    def clean_tweets(self):
        start = timer()
        self.df.text = self.df.text.apply(TweetCleaner.strip_links)
        self.df.text = self.df.text.apply(TweetCleaner.strip_mentions)
        self.df.text = self.df.text.apply(TweetCleaner.strip_hashtags)
        self.df.text = self.df.text.apply(TweetCleaner.strip_rt)
        self.df.text = self.df.text.apply(
            TweetCleaner.remove_special_characters)
        end = timer()
        print('Cleaned tweets in {}'.format(end - start))

    def plot(self, top=100):
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_result = vectorizer.fit_transform(self.df['text'])

        scores = zip(vectorizer.get_feature_names(),
                     np.asarray(tfidf_result.sum(axis=0)).ravel())

        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)

        labels, scores = [], []

        # Get the scores and labels of the top 100 tweets
        for item in sorted_scores[:top]:
            print("{0:50} Score: {1}".format(item[0], item[1]))
            # sns.distplot(item[1], label=item[0])
            labels.append(item[0])
            scores.append(item[1])

        # y_pos = np.arange(len(scores))

        # plt.bar(np.arange(max(scores)), scores, color="blue")
        # plt.xticks(y_pos, labels)
        # plt.show()


ta = TweetAnalyzer()
ta.plot()
# ta.get_sentiments()

# best_threshold = -1
# best_accuracy = -1
# best_index = -1

# for index, result in enumerate(results):

# # 	df, features, threshold = result['df'], result['features'], result['threshold']
#     features, threshold = result['features'], result['threshold']


# 	print('Fitting for threshold = {}'.format(threshold))

# 	# K-fold construction
# 	folds = 10
# 	kf = model_selection.KFold(n_splits=folds, shuffle=True)

# 	# K-fold cross validation and performance evaluation
# 	foldid = 0
# 	totacc = 0.
# 	ytlog = []
# 	yplog = []

# 	for train_index, test_index in kf.split(df.airline_sentiment):
# 		foldid += 1
# 		print("Starting Fold %d" % foldid)
# 		print("\tTRAIN:", len(train_index), "TEST:", len(test_index))
# 		X_train, X_test = features[train_index], features[test_index]
# 		y_train, y_test = df.airline_sentiment[train_index], df.airline_sentiment[test_index]

# 		clf.fit(X_train, y_train)
# 		y_pred = clf.predict(X_test)

# 		acc = accuracy_score(y_pred, y_test)
# 		totacc += acc
# 		ytlog += list(y_test)
# 		yplog += list(y_pred)

# 		print('\tAccuracy:', acc)

#     print("Average Accuracy: %0.3f" % (totacc / folds,))

# 	if (totacc / folds) > best_accuracy:
# 		best_accuracy = totacc / folds
# 		best_threshold = threshold
# 		best_index = index

# 	print(classification_report(ytlog, yplog, target_names=df.airline_sentiment))


# print('\n\n The best accuracy was {} using a threshold of {}'.format(best_accuracy, best_threshold))
