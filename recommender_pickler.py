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


def pickleModel(model):
    """Pickles model provided."""
    model.save('pickle/recommender.pkl')


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
    item_data.rename(columns={'hike_id': 'hike_id'}, inplace=True)
    item_data = item_data.dropna()
    item_sf = gl.SFrame(item_data)

    model = buildFinalRecommender(sf, item_sf)
    pickleModel(model)
    print "Recommendation model pickled"
