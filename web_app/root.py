from flask import Flask, url_for, request, render_template, Markup,redirect
from pymongo import MongoClient
#from src.sentimentAnalysis import detect_sentiment, Rating
import cPickle as pickle
from recommender import itemContentRecommender
#from apscheduler.schedulers.background import BackgroundScheduler
#from apscheduler.triggers.interval import IntervalTrigger





app = Flask(__name__)
PORT = 8080
'''
scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=reRunRecommender,
    trigger=IntervalTrigger(seconds=1800),
    id='rerun fac_model',
    name='Reruns recommender fac_model with new trip report data every 30 minutes',
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
	fac_model = gl.recommender.ranking_factorization_recommender.create(sf, user_id='author_id',
                                                                    item_id='hike_id', target='Rating',
                                                                    regularization=1e-5,
                                                                    linear_regularization=1e-8)
	fac_model.save('pickle/recommender.pkl')

'''


@app.route('/')
def root():

	return render_template('index.html')


@app.route('/recommender', methods=['GET', 'POST'])
def getNewRatings():
	hikes = db.hikes.find({})
	return render_template('recommender.html', hikes=hikes)


@app.route('/my-recommendations', methods=['POST', 'GET'])
def getRecs():
    """DOC STRING."""
    hike_id = hike_ider[request.args.get('hike-name')]
    ic_model.likeHike(hike_id)
    my_recs = ic_model.recommend(5)
    recs = db.hikes.find({"hike_id": {"$in": list(my_recs['hike_id'])}})

    return render_template('my-recommendations.html', recs=recs)

# Shut down the scheduler when exiting the app
#atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    # Register for pinging service

    # Connect to the database
    client = MongoClient()
    db = client['wta']
    with open('pickle/ic_recommender.pkl', 'rb') as icfp:
        ic_model = pickle.load(icfp)


    # Get the fac_model
    with open('pickle/ider.pkl') as f:
    	hike_ider = pickle.load(f)

    # Start Flask app
    app.run(host='0.0.0.0', port=PORT, threaded=True)
