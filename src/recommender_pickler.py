"""Builds and pickles the recommender for the web application."""
from recommender import itemContentRecommender
import pandas as pd
import cPickle as pickle


def buildItemContentRecommender(item_data, weights):
    """Create the recommender model from item feature dataframe.

    item_data (Pandas Dataframe):  Dataframe of hike features.
    weights (Dictionary):  Dictionary of weight to apply to each of item df columns.

    Output: Recommender model
    """
    model = itemContentRecommender(item_data, weights=weights)
    return model


def normalize(item_data, col):
    """Normalize the give column of the provided dataframe.


    item_data (Pandas Dataframe):  Dataframe of hike features.
    col (String): Name of column to normalize.
    """
    item_data[col] = (item_data[col] - item_data[col].mean())/(item_data[col].max() - item_data[col].min())


if __name__ == '__main__':
    # Load and prepare the item dataframe
    item_data = pd.read_csv('../data/itemData.csv')
    item_data = item_data.drop(labels=['Unnamed: 0', 'hike_name'], axis=1)
    for col in [c for c in item_data.columns if c not in [u'hike_id']]:
        normalize(item_data, col)
    item_data = item_data.dropna()

    # load weights
    with open('../pickle/weights.pkl', 'rb') as f:
        weights = pickle.load(f)

    # build item content recommender model
    ic_model = buildItemContentRecommender(item_data, weights)

    # pickle the item content recommender model
    with open('../pickle/ic_recommender.pkl', 'w') as pfp:
        pickle.dump(ic_model, pfp)

    print "Item Recommendation model pickled"
