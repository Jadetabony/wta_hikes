import scipy.stats as scs
import pandas as pd
import numpy as np




class itemContentRecommender(object):

    def fit(self, df, id_column, weights=None):
        self.df = df
        self.id_column = id_column
        self.weights = weights

    def recommend(self, id_num, k, distance='cosine', apply_weights=True):
        if apply_weights:
            for col in self.weights.keys():
                df[col]=df[col] * weights[col]
        if distance=='cosine':
            
