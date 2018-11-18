from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation, TruncatedSVD
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import json
import jsonlines
from TweetPreprocessor import TweetPreprocessor
from timeit import default_timer as timer



TWEETS_FILE = 'user_tweets.jsonl'
DEBUG = True
#Building features from raw data



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
        self.tfidf_result = None
        self.feature_names = None
        self.df = pd.DataFrame(self.tweets, columns=columns)
        self.clean_tweets()
        if DEBUG:
            print(self.df.head())

    def clean_tweets(self):
        start = timer()
        self.df.text = self.df.text.apply(TweetPreprocessor.strip_links)
        self.df.text = self.df.text.apply(TweetPreprocessor.strip_mentions)
        self.df.text = self.df.text.apply(TweetPreprocessor.strip_hashtags)
        self.df.text = self.df.text.apply(TweetPreprocessor.strip_rt)
        self.df.text = self.df.text.apply(
            TweetPreprocessor.remove_special_characters)
        end = timer()
        print('Cleaned tweets in {}'.format(end - start))

    def vectorize(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_result = self.vectorizer.fit_transform(self.df['text'])
        self.feature_names = self.vectorizer.get_feature_names()

    def top_n(self, top=100):
        if self.feature_names is None or self.tfidf_result is None:
            print('Must run vectorize() first before calling top_n')
            return

        scores = zip(self.feature_names,
                     np.asarray(self.tfidf_result.sum(axis=0)).ravel())

        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)

        labels, scores = [], []

        # Get the scores and labels of the top 100 tweets
        for item in sorted_scores[:top]:
            print("{0:50} Score: {1}".format(item[0], item[1]))
            # sns.distplot(item[1], label=item[0])
            labels.append(item[0])
            scores.append(item[1])

        index = np.arange(len(scores))
        plt.bar(index, scores)
        plt.xlabel('Word', fontsize=12)
        plt.ylabel('TFIDF Score', fontsize=12)
        plt.xticks(index, labels, fontsize=8, rotation=90)
        plt.title('Top {} features'.format(top))
        plt.savefig('Top_{}'.format(top))

    def topic_model(self, num_topics=10):
        if DEBUG:
            print('Performing topic modeling with {} topics'.format(num_topics))

        # Build a Latent Dirichlet Allocation Model
        self.lda_model = LatentDirichletAllocation(n_topics=num_topics, max_iter=10, learning_method='online')
        lda_Z = self.lda_model.fit_transform(self.tfidf_result)
        print('LDA shape: ')
        print(lda_Z.shape)  # (NO_DOCUMENTS, NO_TOPICS)

        # Build a Non-Negative Matrix Factorization Model
        self.nmf_model = NMF(n_components=num_topics)
        nmf_Z = self.nmf_model.fit_transform(self.tfidf_result)
        print('NMF shape: ')
        print(nmf_Z.shape)  # (NO_DOCUMENTS, NO_TOPICS)

        # Build a Latent Semantic Indexing Model
        self.lsi_model = TruncatedSVD(n_components=num_topics)
        lsi_Z = self.lsi_model.fit_transform(self.tfidf_result)
        print('LSI shape: ')
        print(lsi_Z.shape)  # (NO_DOCUMENTS, NO_TOPICS)

        if DEBUG:
            # Let's see how the first document in the corpus looks like in different topic spaces
            print("LDA Model:")
            self.print_topics(self.lda_model)
            print("=" * 20)

            print("NMF Model:")
            self.print_topics(self.nmf_model)
            print("=" * 20)

            print("LSI Model:")
            self.print_topics(self.lsi_model)
            print("=" * 20)

    # Helper function to print topics
    def print_topics(self, model, top_n=10):
        for idx, topic in enumerate(model.components_):
            print("Topic %d:" % (idx))
            print([(self.vectorizer.get_feature_names()[i], topic[i])
                            for i in topic.argsort()[:-top_n - 1:-1]])

    def plot_topic_model_SVD(self):
        from bokeh.io import push_notebook, show, output_notebook
        from bokeh.plotting import figure
        from bokeh.models import ColumnDataSource, LabelSet
        output_notebook()

        self.svd = TruncatedSVD(n_components=2)
        words_2d = self.svd.fit_transform(self.tfidf_result.T)

        df = pd.DataFrame(columns=['x', 'y', 'word'])
        df['x'], df['y'], df['word'] = words_2d[:,0], words_2d[:,1], self.feature_names

        source = ColumnDataSource(ColumnDataSource.from_df(df))
        labels = LabelSet(x="x", y="y", text="word", y_offset=8,
                        text_font_size="8pt", text_color="#555555",
                        source=source, text_align='center')

        plot = figure(plot_width=600, plot_height=600)
        plot.circle("x", "y", size=12, source=source, line_color="black", fill_alpha=0.8)
        plot.add_layout(labels)
        show(plot, notebook_handle=True)


ta = TweetAnalyzer()
ta.vectorize()
# ta.top_n(100)
ta.topic_model()
ta.plot_topic_model_SVD()

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
