# NOTE: Tweet cleaning code was taken from Lab in class

import re
import unicodedata
import string
import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np
np.random.seed(2018)
import nltk
nltk.download('wordnet')


# Static class that cleans the tweets
class TweetPreprocessor:

    @staticmethod
    def strip_links(text):
        link_regex = re.compile(
            '((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
        links = re.findall(link_regex, text)
        for link in links:
            text = text.replace(link[0], ', ')
        return text

    @staticmethod
    def strip_mentions(text):
        entity_prefixes = ['@']
        for separator in string.punctuation:
            if separator not in entity_prefixes:
                text = text.replace(separator, ' ')
        words = []
        for word in text.split():
            word = word.strip()
            if word:
                if word[0] not in entity_prefixes:
                    words.append(word)
        return ' '.join(words)

    @staticmethod
    def strip_hashtags(text):
        entity_prefixes = ['#']
        for separator in string.punctuation:
            if separator not in entity_prefixes:
                text = text.replace(separator, ' ')
        words = []
        for word in text.split():
            word = word.strip()
            if word:
                if word[0] not in entity_prefixes:
                    words.append(word)
        return ' '.join(words)

    @staticmethod
    def strip_rt(text):
        return text.replace('RT', '')

    @staticmethod
    def remove_special_characters(text, remove_digits=True):
        pattern = r'[^a-zA-z0-9\s]' if not remove_digits else r'[^a-zA-z\s]'
        text = re.sub(pattern, '', text)
        text = unicodedata.normalize('NFKD', text).encode(
            'ascii', 'ignore').decode('utf-8', 'ignore')
        return text

    # Helper method called by
    def lemmatize_stemming_helper(text):
        return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

    @staticmethod
    def lemmatize_stemming(text):
        result = []
        for token in gensim.utils.simple_preprocess(text):
            if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
                result.append(lemmatize_stemming_helper(token))
        return result
