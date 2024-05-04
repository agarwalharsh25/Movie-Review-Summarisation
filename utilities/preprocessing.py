import itertools
import re
import unicodedata
from string import punctuation

import nltk

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def tokenize_sentences(text):
    return nltk.sent_tokenize(text)


def tokenize_words(text):
    return nltk.word_tokenize(text)


def remove_non_ascii_characters(words):
    return [
        unicodedata.normalize('NFKD',
                              word).encode('ascii',
                                           'ignore').decode('utf-8', 'ignore')
        for word in words
    ]


def remove_punctuations(words):
    return [word for word in words if word not in punctuation]


def lemmatize_words(words):
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(word) for word in words]


def transform_words_to_lowercase(words):
    return [word.lower() for word in words]


def remove_stopwords(words):
    return [word for word in words if word not in stopwords.words('english')]


def get_preprocess_text(text):
    text = re.sub(r'<[^>]+>', '', text)
    text = text.strip()
    text = re.sub(' +', ' ', text)

    sentences = tokenize_sentences(text)
    words = [tokenize_words(sentence) for sentence in sentences]
    words = list(itertools.chain.from_iterable(words))

    # remove non ascii characters
    words = remove_non_ascii_characters(words)

    # remove punctuations
    # words = remove_punctuations(words)

    # lemmatize words
    words = lemmatize_words(words)

    # lowercase
    words = transform_words_to_lowercase(words)

    # remove stopwords
    # words = remove_stopwords(words)

    return " ".join(words)
