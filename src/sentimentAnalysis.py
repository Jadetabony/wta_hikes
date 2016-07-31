"""Takes hike text and returns the sentiment rating."""

from __future__ import division
from textblob import TextBlob
import string
import re


def detect_sentiment(text):
    text = re.sub(r'/\u\d+', '', text)
    text = ''.join([char for char in text if char not in string.punctuation])
    return TextBlob(text.encode('ascii', 'ignore') ).sentiment.polarity

def setRating(sentiment):
    """Sets rating based on textblob sentiment"""
    if sentiment < 0.0741324307501:
        return 1
    elif sentiment < 0.12879503367:
        return 2
    elif sentiment < 0.179433020683:
        return 3
    elif sentiment < 0.25:
        return 4
    else:
        return 5
