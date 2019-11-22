import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import wordnet,stopwords
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd


lemmatizer = WordNetLemmatizer()
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('stopwords')


def work_with_text(text, withLemmatizer = False):
    # Convert text
    sentences = nltk.sent_tokenize(text)

    # Remove "stop-words" like "I, have, may... etc"
    stop_words = set(stopwords.words("english"))

    # From array of texts
    without_stop_words = []
    for i in sentences:
        words = nltk.word_tokenize(i.lower())
        without_stop_words += [word for word in words if not word in stop_words]
    # Lemmatize
    if not withLemmatizer:
        return_array = without_stop_words
    else:
        return_array = []
        for word in without_stop_words:
            return_array.append(lemmatizer.lemmatize(word, wordnet.VERB))

    # Bag test
    # work_with_bag(return_array)

    # Return array of words
    return return_array


def work_with_bag(text):
    count_vectorizer = CountVectorizer()
    bag_of_words = count_vectorizer.fit_transform(text)
    feature_names = count_vectorizer.get_feature_names()
    pd.DataFrame(bag_of_words.toarray(), columns=feature_names)


