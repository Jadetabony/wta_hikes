import graphlab as gl
import pandas as pd
from src.sentimentAnalysis import detect_sentiment, setRating
import cPickle as pickle
import random

def unpickleIder(pickledId):
    with open(pickledId, 'rb') as fid:
        ider = pickle.load(fid)
    return ider

def unpickleRecommender(pickledmodel):
    model = gl.load_model(pickledmodel)
    return model

def getRecommendation(model, ider, itemDf,  with_rec=True,numRecommendations=5):
    """Gets new TR for a specific hike to input into TR df for recommender model"""
    user = random.randint(333333, 2222222)
    if not with_rec:
        recs = model.recommend(users=[user])
    else:
        hike_name = raw_input('Hike name: ')
        hike_id = ider[hike_name]
        rate_prompt = raw_input('Would you like to input a rating or trip report? (Enter r or tr): ')
        if rate_prompt == 'tr':
            text = raw_input('Input trip report: ')
            rating = setRating(detect_sentiment(text))
        else:
            rating = int(raw_input('Input hike rating: '))
        new_instance = pd.DataFrame.from_dict({'hike_id': [hike_id], 'author_id': [user], 'Rating': [rating]})
        sf = gl.SFrame(new_instance)
        recs = model.recommend(users=[user], new_observation_data=sf, )
    return recs


def printRecs(item_datarecs):
    """Formats the recommendations to be printed with the name, elevation change, mileage and
    drive time from Seattle"""
    for h in [f for f in recs['hike_id']]:
        row = item_data[item_data['hike_id'] == h]
        print '**', row['hike_name'].values[0], '**'
        print 'Total Distance: ', row['total_dist'].values[0]
        print 'Elevation Gain: ', row['elevation gain'].values[0]
        print 'Driving time from Seattle (minutes): ', row['time_from_seattle'].values[0]
        print '----------------------------------------------------------------'


if __name__ == '__main__':
    item_data = pd.read_csv('data/itemData.csv')
    item_data = item_data.drop(labels=['Unnamed: 0'], axis=1)

    model = unpickleRecommender('pickle/recommender.pkl')
    ider = unpickleIder('pickle/ider.pkl')
    recs = getRecommendation(model, ider, item_data, with_rec=True)
    printRecs(recs)
