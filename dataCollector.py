""" Collects all of the wta hike data and trip reports.  Stores them in data folder.
NOTE!! Builds dataset from scratch.  Should not use if you have already built dataset.
Use dataUpdate.py if you already have the dataset.
NOTE!! You will need your own Google API key to run the cleaner and obtain time from Seattle."""

from pymongo import MongoClient
import pandas as pd
from src.wtaScraper import collect_hikeurls, build_dataset, getHikeDescription
from src.tripReportScraper import TripReportBuilder
from src.dataCleaning import cleanData

if __name__ == '__main__':
    #collect hike metadata.  Stores it in washington_hikes.csv
    urls = collect_hikeurls('http://www.wta.org/go-hiking/hikes')
    data = pd.read_csv('washington_hikes.csv')
    build_dataset(data, urls)
    data = pd.read_csv('washington_hikes.csv')
    getHikeDescription(data)

    #cleans washington_hikes and stores in washington_hikes_clean.csv
    cleanData(data)

    #collect trip reports into MongoDB
    df = pd.read_csv('data/washington_hikes_clean.csv')
    client = MongoClient()
    db = client.wta
    db.trip_reports.drop()
    TripReportBuilder(df)
