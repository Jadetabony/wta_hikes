"""Creates a recommender object that keeps track of the hikes liked and
returns recommendations based on pairwise cosine similarity."""
import pandas as pd
import numpy as np
from weighted_pairwise_similarity import pairwise_cosine_similarity
from sklearn.metrics.pairwise import cosine_similarity


class itemContentRecommender(object):
    """Creates a recommender object that keeps track of the hikes liked and
    returns recommendations based on pairwise cosine similarity."""

    def __init__(self, hikes, weights=None):
        """Initiates the hike recommender object.

        Hikes (pandas dataframe): DataFrame of the hikes with all of their features, normalized
        weights (dictionary): Dictionary of weights, keys are the column names as found in X and y. Values are the weights to be applied

        """
        self.hike_matrix = hikes
        self.feature_weights = weights
        self.hikes_liked = []
        self.hikes_disliked = []
        self.weights = weights



    def likeHike(self, hike_id):
        """Adds liked hike to the hikes_liked array.

        If no hikes have been liked already, creates the hikes_liked array.
        Else, adds liked hike to the hikes_liked array. Then drops the liked
        hike from the hike matrix.  Resets index after each addition.

        hike_id (int): Id number that corresponds to the hike

        Output: None
        """

        indx = self.hike_matrix[self.hike_matrix['hike_id'] == hike_id].index[0]
        if len(self.hikes_liked) == 0:
            self.hikes_liked = pd.DataFrame(self.hike_matrix.ix[indx]).T
            self.hike_matrix = self.hike_matrix.drop(indx, axis=0).reset_index(drop=True)
        else:
            self.hikes_liked = self.hikes_liked.append(self.hike_matrix.ix[indx])
            self.hike_matrix = self.hike_matrix.drop(indx, axis=0).reset_index(drop=True)


    def unlikeHike(self, hike_id):
        "Removes hike from list of hikes that have been liked."

        self.hikes_liked = self.hikes_liked.drop(labels=[hike_id])


    def hikesLiked(self):
        """Prints the list of hikes that have already been liked."""

        print self.hikes_liked


    def recommend(self, n=5):
        """Returns recommendations based on average cosine similarity.

        Calculates the cosine similarity between all of the liked hiles and the matrix of hikes that are not liked.
        The average cosine similarity is they taken and the top 5 (closest to a cosine similarity of 1) are returned.

        n (int): Number of recommendations.

        Output: n number of recommendations."""
        # Creates a pandas series of the hike id numbers so that the index
        # can be matched back to the hike number
        hike_number = self.hike_matrix['hike_id']
        # drop hike id numbers to avoid affecting cosine similarity calculations
        X = self.hike_matrix.drop('hike_id', axis=1)
        y = self.hikes_liked.drop('hike_id', axis=1)
        # passes the X and y matrix through the pairwise cosine similarity,
        # sorts it and grabs the last n items
        # the precense of weights determines which function is used
        if not self.weights:
            cs = cosine_similarity(X, y).mean(axis=1)
            rec_index = np.argsort(cs)[-n:][::-1]
            recommendations = hike_number.ix[rec_index]
        else:
            cs = pairwise_cosine_similarity(X, y, self.weights).mean(axis=1)
            rec_index = np.argsort(cs)[-n:][::-1]
            recommendations = hike_number.ix[rec_index]
        return recommendations
