import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import wordnet,stopwords
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd


lemmatizer = WordNetLemmatizer()
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('stopwords')


def remove_stop_words(text):
    sentences = nltk.sent_tokenize(text)
    stop_words = set(stopwords.words("english"))
    without_stop_words = []
    for i in sentences:
        words = nltk.word_tokenize(i.lower())
        without_stop_words += [word for word in words if not word in stop_words]
    return without_stop_words


def lemmatize(array):
    return_array = []
    for word in array:
        return_array.append(lemmatizer.lemmatize(word, wordnet.VERB))
    return return_array


def work_with_bag(text):
    count_vectorizer = CountVectorizer()
    bag_of_words = count_vectorizer.fit_transform(text)
    feature_names = count_vectorizer.get_feature_names()
    pd.DataFrame(bag_of_words.toarray(), columns=feature_names)


