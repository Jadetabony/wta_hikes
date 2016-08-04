import graphlab as gl
import pandas as pd
import numpy as np


def buildFinalRecommender(sf, item_sf):
    """Creates the recommender model from sf and item_sf.

    Parameters:

    sf: GraphLab SFrame.  Dataframe of hike id, user id and ratings.
    item_sf: GraphLab SFrame.  Dataframe of the hike information.
    """
    model = gl.recommender.ranking_factorization_recommender.create(sf, user_id='author_id',
                                                                    item_id='hike_id', target='Rating',
                                                                    regularization=1e-5,
                                                                    linear_regularization=1e-8)
    return model


def buildItemContentRecommender(sf, item_sf=None):
    """Creates the recommender model from sf and item_sf.

    Parameters:

    sf: GraphLab SFrame.  Dataframe of hike id, user id and ratings.
    item_sf: GraphLab SFrame.  Dataframe of the hike information.
    """
    model = gl.recommender.item_content_recommender.create(sf, 'hike_id')
    return model

def pickleModel(model, fname):
    """Pickles model provided."""
    model.save(fname)

def norm(df, col):
    """Normalized the give column of the provided dataframe"""
    df[col] = (df[col] - df[col].mean())/(df[col].max() - df[col].min())


if __name__ == '__main__':
    # Load and prepare the ratings dataframe
    df = pd.read_csv(open('data/tripReports.csv', 'rU'), encoding='utf-8', engine='c')
    df = df.drop(labels=['Unnamed: 0', 'Name', 'Text', 'Date','Creator', 'TextBlobSentiment', 'GraphLabSentiment', 'TrainedModelSentiment'], axis=1)
    df = df.dropna()
    df['hike_id'] = df['hike_id'].fillna(np.nan).astype(int)
    df['author_id'] = df['author_id'].fillna(np.nan).astype(int)
    sf = gl.SFrame(df)

    # Load and prepare the item dataframe
    item_data = pd.read_csv('data/itemData.csv')
    item_data = item_data.drop(labels=['Unnamed: 0'], axis=1)
    norm(item_data, 'elevation gain')
    norm(item_data, 'time_from_seattle')
    norm(item_data, 'numReports')
    norm(item_data, 'total_dist')
    item_data = item_data.dropna()
    item_sf = gl.SFrame(item_data)

    model = buildFinalRecommender(sf, item_sf)
    pickleModel(model, 'pickle/recommender.pkl')
    print "Recommendation model pickled"
    item_model = buildItemContentRecommender(item_sf)
    pickleModel(item_model, 'pickle/itemContRecommender.pkl')
    print "Item Sim Recommendation model pickled"
