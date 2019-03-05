from __future__ import division
import cPickle as picle
import numpy as np
import string
import re


def mongo2PandasClean(mongodb, drop_id=True):
    df = pd.DataFrame(list(mongodb.find()))
    if drop_id:
        del df['_id']
    return df

def detect_sentiment(text, tfidf, sa_model):
    """Parses through text data to make it readable by TextBlob and outputs the
    sentiment rating according to TextBlob [-1, 1].

    **Input parameters**
    ------------------------------------------------------------------------------
    text: string.

    **Output**
    ------------------------------------------------------------------------------
    probability of positive sentiment: float between [0, 1]
    """
    X = tfidf.transform(df['Text'])
    return model.predict_proba(X)


def useCutoffs(num, cutoff):
    """Assigns 1-5 star rating based on provided cutoff points.

    **Input parameters**
    ------------------------------------------------------------------------------
    num: float. Sentiment analysis.

    cutoff: list.  n=3.  List of cutoff values for ratings.

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
    return [useCutoffs(num, cutoffs) for num in df[sentiment_column]]


if __name__ == '__main__':
    # Load and prepare the ratings dataframe
    connection = MongoClient()
    db = connection.wta
    df = mongo2PandasClean(db.trip_reports)

    with open('../pickle/vectorizer.pkl', 'rb') as fid:
        tfidf = pickle.load(fid)
    with open('../pickle/SAmodel.pkl', 'rb') as fid:
        model = pickle.load(fid)

    df['sentiment_score'] = [detect_sentiment(t, tfidf, model) for t in df['Text']]
    df['Rating'] = setRating(df, 'sentiment_score')

    df.to_csv('../data/tripReports.csv')
