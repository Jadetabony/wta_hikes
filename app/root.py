from flask import Flask, url_for, request, render_template, Markup,redirect
from pymongo import MongoClient
import graphlab as gl
import pandas as pd
#from src.sentimentAnalysis import detect_sentiment, Rating
from datetime import date
import cPickle as pickle
import time
import atexit
#from apscheduler.schedulers.background import BackgroundScheduler
#from apscheduler.triggers.interval import IntervalTrigger




'''import json
from json2html import json2html
import requests
import socket
import time
from datetime import datetime
from src.model import MyModel
from src.predict import predict

import cPickle as pickle
import pandas as pd'''


app = Flask(__name__)
PORT = 8080
'''
scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=reRunRecommender,
    trigger=IntervalTrigger(seconds=1800),
    id='rerun model',
    name='Reruns recommender model with new trip report data every 30 minutes',
    replace_existing=True)


def mongo2PandasClean(mongodb, drop_id=True):

	"""Imports all of the data from mongodb into a pandas dataframe.  Drops _id field when drop_id is True"""
	df = pd.DataFrame(list(mongodb.find()))
	del df['_id']
	return df


def reRunRecommender():
	"""Rebuilds recommender system and saves it in pickle spot"""
	#get new data
	df = mongo2PandasClean(db.trip_reports)
	df = df.drop(labels=['Text', 'Date', 'Creator', 'hike_name'], axis=1)
	sf = gl.SFrame(df)
	model = gl.recommender.ranking_factorization_recommender.create(sf, user_id='author_id',
                                                                    item_id='hike_id', target='Rating',
                                                                    regularization=1e-5,
                                                                    linear_regularization=1e-8)
	model.save('pickle/recommender.pkl')

'''


@app.route('/')
def api_root():
	my_recs = model.recommend(users=[db.users.count()+1], k=6)
	recs = db.hikes.find({"hike_id": {"$in": list(my_recs['hike_id'])}})
	return render_template('index.html', recs=recs)


@app.route('/returning-user', methods=['GET', 'POST'])
def getReturnRatings():
	hikes = db.hikes.find({})
	return render_template('recommender.html', hikes=hikes)


@app.route('/new-user', methods=['GET', 'POST'])
def getNewRatings():
	hikes = db.hikes.find({})
	return render_template('recommender.html', hikes=hikes)


@app.route('/my-recommendations', methods=['POST', 'GET'])
def getRecs():
	hike_id = hike_ider[request.args.get('hike-name')]
	if request.args.get('username')=='':
		my_recs = model.get_similar_items(items=[hike_id], k=5)
		recs = db.hikes.find({"hike_id": {"$in": list(my_recs['similar'])}})
	elif db.users.find({'username': request.args.get('username')}).count()==0:
		db.trip_reports.insert({'Creator': request.args.get('username'), 'Date': date.today().strftime("%B %d, %Y"), 'hike_name': request.args.get('hike-name'), 'Text': request.args.get('tripReport'),
                       'author_id': db.users.count()+1, 'hike_id': hike_id, 'Rating': request.args.get('rating')})
		my_recs = model.get_similar_items(items=[hike_id], k=5)
		recs = db.hikes.find({"hike_id": {"$in": list(my_recs['similar'])}})
	else:
		user = int(db.users.find_one({'username': request.args.get('username')})['id'])
		db.trip_reports.insert({'Creator': request.args.get('username'), 'Date': date.today().strftime("%B %d, %Y"), 'hike_name': request.args.get('hike-name'), 'Text': request.args.get('tripReport'),
                       'author_id': user, 'hike_id': hike_id, 'Rating': request.args.get('rating')})
		new_instance = pd.DataFrame.from_dict({'hike_id': [hike_id], 'author_id': [user], 'Rating': [int(request.args.get('rating'))]})
		sf = gl.SFrame(new_instance)
		my_recs = model.recommend(users=[user], new_observation_data=sf, k=5)
		recs = db.hikes.find({"hike_id": {"$in": list(my_recs['hike_id'])}})
	return render_template('my-recommendations.html', recs=recs)

# Shut down the scheduler when exiting the app
#atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
	# Register for pinging service

	# Connect to the database
	client = MongoClient()
	db = client['wta']
	model = gl.load_model('pickle/recommender.pkl')
	# Get the model
	with open('pickle/ider.pkl') as f:
		hike_ider = pickle.load(f)

	# Start Flask app
	app.run(host='0.0.0.0', port=PORT, debug=True)
