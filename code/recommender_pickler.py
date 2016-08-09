import graphlab as gl
import pandas as pd
import numpy as np
import cPickle as pickle


def buildFactRecommender(sf, item_sf):
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

def buildItemContentRecommender(item_sf, weights):
    """Creates the recommender model from sf and item_sf.

    Parameters:

    sf: GraphLab SFrame.  Dataframe of hike id, user id and ratings.
    item_sf: GraphLab SFrame.  Dataframe of the hike information.
    """
    model = gl.recommender.item_content_recommender.create(item_sf, item_id='hike_id', weights=weights)
    return model

def pickleModel(model, fname):
    """Pickles model provided."""
    model.save(fname)

def norm(df, col):
    """Normalized the give column of the provided dataframe"""
    df[col] = (df[col] - df[col].mean())/(df[col].max() - df[col].min())


if __name__ == '__main__':
    # Load and prepare the ratings dataframe
    df = pd.read_csv(open('../data/tripReports.csv', 'rU'), encoding='utf-8', engine='c')
    df = df.drop(labels=['Unnamed: 0', 'hike_name', 'Text', 'Date','Creator'], axis=1)
    df = df.dropna()
    df['hike_id'] = df['hike_id'].fillna(np.nan).astype(int)
    df['author_id'] = df['author_id'].fillna(np.nan).astype(int)
    sf = gl.SFrame(df)

    # Load and prepare the item dataframe
    item_data = pd.read_csv('../data/itemData.csv')
    item_data = item_data.drop(labels=['Unnamed: 0', 'hike_name'], axis=1)
    norm(item_data, 'elevation gain')
    norm(item_data, 'time_from_seattle')
    norm(item_data, 'numReports')
    norm(item_data, 'total_dist')
    item_data = item_data.dropna()
    item_sf = gl.SFrame(item_data)

    #load weights
    with open('../pickle/weights.pkl', 'rb') as f:
        weights = pickle.load(f)

    model = buildFactRecommender(sf, item_sf)
    pickleModel(model, '../web_app/pickle/recommender.pkl')
    print "Recommendation model pickled"

    ic_model = buildItemContentRecommender(item_sf, weights)
    pickleModel(ic_model, '../web_app/pickle/itemcontrecommender.pkl')
    print "Item Recommendation model pickled"
