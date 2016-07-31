import graphlab as gl
import pandas as pd
from src.sentimentAnalysis import detect_sentiment, setRating



def unpickleRecommender(pickledmodel):
    model = gl.load_model(pickledmodel)
    return model

def getRecommendation(model, itemDf, numRecommendations=5):
    """Gets new TR for a specific hike to input into TR df for recommender model"""
    hike_name = raw_input('Hike name: ')
    hike_id = itemDf['HikeId'][itemDf['hike_name'] == hike_name]
    text = raw_input('Input trip report: ')
    rating = setRating(detect_sentiment(text))
    new_instance = pd.DataFrame.from_dict({'HikeId': [hike_id], 'AuthorId': [222222222], 'Rating': [rating]})
    sf = gl.SFrame(new_instance)
    recs = model.recommend(users=[222222222], new_observation_data=sf)
    return recs


def printRecs(item_datarecs):
    """Formats the recommendations to be printed with the name, elevation change, mileage and
    drive time from Seattle"""
    for h in [f for f in recs['HikeId']]:
        row = item_data[item_data['HikeId'] == h]
        print '**', row['hike_name'].values[0], '**'
        print 'Total Distance: ', row['total_dist'].values[0]
        print 'Elevation Gain: ', row['elevation gain'].values[0]
        print 'Driving time from Seattle (minutes): ', row['time_from_seattle'].values[0]
        print '----------------------------------------------------------------'

if __name__ == '__main__':
    item_data = pd.read_csv('data/itemData.csv')
    item_data = item_data.drop(labels=['Unnamed: 0'], axis=1)
    item_data.rename(columns={'hike_id': 'HikeId'}, inplace=True)
    item_data.dropna(inplace=True)

    model = unpickleRecommender('pickle/recommender.pkl')
    recs = getRecommendation(model, item_data)
    printRecs(recs)
