import graphlab as gl
import pandas as pd
import cPickle as pickle
import numpy as np


def buildFinalRecommender(sf, item_sf):
    model = gl.recommender.factorization_recommender.create(sf, user_id='AuthorId', item_id='HikeId', target='Rating', solver='sgd', item_data=item_sf)
    return model


def pickleModel(model):
    model.save('pickle/recommender.pkl')

if __name__ == '__main__':
    # Load and prepare the ratings dataframe
    df = pd.read_csv(open('data/tripReports.csv', 'rU'), encoding='utf-8', engine='c')
    df = df.drop(labels=['Unnamed: 0', 'Name', 'Text', 'Data', 'Author', 'TextBlobSentiment'], axis=1)
    df = df.dropna()
    df['HikeId'] = df['HikeId'].fillna(np.nan).astype(int)
    df['AuthorId'] = df['AuthorId'].fillna(np.nan).astype(int)
    sf = gl.SFrame(df)

    # Load and prepare the item dataframe
    item_data = pd.read_csv('data/itemData.csv')
    item_data = item_data.drop(labels=['Unnamed: 0'], axis=1)
    item_data.rename(columns={'hike_id': 'HikeId'}, inplace=True)
    item_data = item_data.dropna()
    item_sf = gl.SFrame(item_data)

    model = buildFinalRecommender(sf, item_sf)
    pickleModel(model)
    print "Recommendation model pickled"
