"""Takes hike text and returns the sentiment rating."""

from __future__ import division
from textblob import TextBlob
import string
import re


def detect_sentiment(text):
    text = re.sub(r'/\u\d+', '', text)
    text = ''.join([char for char in text if char not in string.punctuation])
    return TextBlob(text.encode('ascii', 'ignore') ).sentiment.polarity
