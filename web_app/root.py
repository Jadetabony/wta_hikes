from flask import Flask, url_for, request, render_template, Markup, redirect
import json
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


def norm(df, col):
    """Normalized the give column of the provided dataframe"""
    df[col] = (df[col] - df[col].mean()) / (df[col].max() - df[col].min())


class HikeRecommender(object):
    def __init__(self, hikes, weights=None):
        self.hike_matrix = hikes
        self.feature_weights = weights
        self.hikes_liked = pd.DataFrame(columns=hikes.columns)
        self.hikes_disliked = pd.DataFrame(columns=hikes.columns)
        if not weights:
            self.weights = {c: 1 for c in hikes.columns}
        else:
            self.weights = weights
            self.weighted_hike_matrix = self.apply_weights()

    def like_hike(self, hike_id):
        indx = self.hike_matrix[self.hike_matrix['hike_id'] == hike_id[0]].index[0]
        self.hikes_liked = self.hikes_liked.append(self.hike_matrix.iloc[indx])
        self.hike_matrix = self.hike_matrix.drop(indx, axis=0).reset_index(drop=True)

    def recommend(self, n=5, apply_weights=True):
        # Calculate similarity to all of the hikes
        # average similarities
        # return top 5
        indx_id = self.hike_matrix['hike_id']
        X = self.hike_matrix.drop('hike_id', axis=1)
        y = self.hikes_liked.drop('hike_id', axis=1)
        cs = cosine_similarity(X, y).mean(axis=1)
        rec_index = np.argsort(cs)[-n:][::-1]
        recommendations = list(indx_id.iloc[rec_index])
        print(recommendations)
        return recommendations

    def apply_weights(self):
        weighted_hike_matrix = pd.DataFrame(columns=self.hike_matrix.columns)
        for col, weight in self.weights.items():
            weighted_hike_matrix[col] = self.hike_matrix[col].apply(lambda x: x * weight)
        return weighted_hike_matrix


app = Flask(__name__)
PORT = 8080


@app.route('/')
def root():
    # my_recs = fac_model.recommend(users=[db.users.count()+1], k=6)
    # recs = db.hikes.find({"hike_id": {"$in": list(my_recs['hike_id'])}})
    return render_template('index.html')


@app.route('/returning-user', methods=['GET', 'POST'])
def getReturnRatings():
    hikes_df = pd.read_csv("../data/itemData.csv")
    hikes = sorted(list(hikes_df['hike_name']))
    return render_template('recommender.html', hikes=hikes)


@app.route('/my-recommendations', methods=['POST', 'GET'])
def getRecs():
    """DOC STRING."""
    hikes_df = pd.read_csv("../data/itemData.csv")
    hike_id = hikes_df[hikes_df['hike_name'] == str(request.args.get('hike-name'))].index.values
    hr.like_hike(hike_id)
    rec_ids = hr.recommend()
    recs = hikes_df.iloc[rec_ids]
    rec_list = []
    for index, row in recs.iterrows():
        rec_list.append(row)
    return render_template('my-recommendations.html', recs=rec_list)


if __name__ == '__main__':
    hike_data = pd.read_csv('../data/itemData.csv')
    item_data = hike_data.drop(labels=['Unnamed: 0', 'hike_name', 'stars'], axis=1)
    item_data.fillna(0, inplace=True)
    # norm(item_data, 'elevation')
    # norm(item_data, 'time_from_seattle')
    # norm(item_data, 'numReports')
    # norm(item_data, 'total_dist')

    # import weights
    with open('../data/weights.json', 'r') as weights_fp:
        weights = json.load(weights_fp)
    hr = HikeRecommender(item_data, weights=weights)
    # Start Flask app
    app.run(host='0.0.0.0', port=PORT, threaded=True)
