"""DOC strings."""
# import packages
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class itemContentRecommender(object):
    """DOC strings."""

    def __init__(self, hikes, weights=None):
        """DOC strings."""
        self.hike_matrix = hikes
        self.feature_weights = weights
        self.hikes_liked = []
        self.hikes_disliked = []
        if self.feature_weights is not None:
            self.applyWeights()

    def applyWeights(self):
        """DOC STRINGS."""
        for key in self.feature_weights.keys():
            self.hike_matrix[key] = self.hike_matrix*self.feature_weights[key]

    def likeHike(self, hike_id):
        """DOC strings."""
        indx = self.hike_matrix[self.hike_matrix['hike_id'] == hike_id].index[0]
        if len(self.hikes_liked) == 0:
            self.hikes_liked = pd.DataFrame(self.hike_matrix.ix[indx]).transpose()
            self.hike_matrix = self.hike_matrix.drop(indx, axis=0).reset_index(drop=True)
        else:
            self.hikes_liked = self.hikes_liked.append(self.hike_matrix.ix[indx])
            self.hike_matrix = self.hike_matrix.drop(indx, axis=0).reset_index(drop=True)

    def recommend(self, n=5):
        """DOC strings."""
        # Calculate similarity to all of the hikes
        # average similarities
        # return top 5
        indx_id = self.hike_matrix['hike_id']
        X = self.hike_matrix.drop('hike_id', axis=1)
        y = self.hikes_liked.drop('hike_id', axis=1)
        cs = cosine_similarity(X, y).mean(axis=1)
        rec_index = np.argsort(cs)[-n:][::-1]
        recommendations = indx_id.ix[rec_index]
        return recommendations
