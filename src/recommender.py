""""DOC strings"""

# import packages
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity



class hikeRecommender(object):

    def __init__(self, hikes, weights=None):
        self.hike_matrix = hikes
        self.feature_weights = weights
        self.hikes_liked = []
        self.hikes_disliked = []
        self.recommendations = []

    def hikeMatrix():



    def likeHike(hike_name):
        self.hikes_liked.append(hike_name)

    def recommend():
        # Calculate similarity to all of the hikes
        # average similarities
        # return top 5


    def calculateSimilarity(X, y):
        return cosine_similarity(X, y)

                #Calculate similarity

    def averageSimilarities(cs_matrix):
        return cs_matrix.mean(axis=1)

    def findClosest(csa_matrix):
        
