from __future__ import division
from textblob import TextBlob
import numpy as np
import string
import re


def detect_sentiment(text):
    """Parses through text data to make it readable by TextBlob and outputs the
    sentiment rating according to TextBlob [-1, 1].

    **Input parameters**
    ------------------------------------------------------------------------------
    text: string.

    **Output**
    ------------------------------------------------------------------------------
    textblob sentiment: float between [-1, 1]
    """
    text = re.sub(r'/\u\d+', '', text)
    text = ''.join([char for char in text if char not in string.punctuation])
    return TextBlob(text.encode('ascii', 'ignore') ).sentiment.polarity


def useRating(num, cutoff):
    """Assigns 1-5 star rating based on provided cutoff points.

    **Input parameters**
    ------------------------------------------------------------------------------
    num: float. Sentiment analysis.

    cutoff: list.  n=5.  List of cutoff values for ratings.

    **Output**
    ------------------------------------------------------------------------------
    Star rating: int. [1, 2, 3, 4 or 5]
    """
    if num < cutoff[0]:
        return 1
    elif num < cutoff[1]:
        return 3
    else:
        return 5


def setRating(df, sentiment_column):
    """Determines cutoff points using the values of the column and then assigns
    rating by calling useRating function.

    **Input parameters**
    ------------------------------------------------------------------------------
    df: pandas dataframe.

    sentiment_column: string.  Column name for sentiment ratings.

    **Output**
    ------------------------------------------------------------------------------
    List of ratings (int) between [1,5]
    """
    cutoffs = [np.percentile(df[sentiment_column], x) for x in [25,75]]
    return [useRating(num, cutoffs) for num in df[sentiment_column]]
