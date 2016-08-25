"""Creates the item dataframe that will be used in the recommender systems from hike df."""

import pandas as pd


def addFeatures(df):
    """Takes the df and creates dummy variables from features column."""
    features = []
    for f in df['features']:
        flist = f.strip('[').strip(']').split(',')
        features.extend(flist)
    features = list(np.unique([f.lstrip() for f in features if f != '']))
    for f in features:
        df[f] = [1 if f in t else 0 for t in df['features']]
    return df


if __name__ == '__main__':
    df = pd.read_csv('../data/washington_hikes_clean_noout.csv')
    df = addFeatures(df)
    df = pd.read_csv('../data/washington_hikes_clean_noout.csv')
    item_data = df[['hike_name', 'hike_id', 'numReports', 'total_dist', 'elevation gain', 'time_from_seattle',
                u'Coast', 'stars', u'Dogs allowed on leash', u'Established campsites', u'Fall foliage',
               u'Good for kids', u'Lakes', u'Mountain views', u'Old growth',
               u'Ridges/passes', u'Rivers', u'Summits', u'Waterfalls',
               u'Wildflowers/Meadows', u'Wildlife']]
    item_data.to_csv('../data/itemData.csv', index_col=0)
