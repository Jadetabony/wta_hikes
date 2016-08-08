"""This file, when called in the terminal will collect all of the trip reports
 for the hikes in the loaded CSV file and load them into a MongoDB"""
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import math
import pandas as pd
from multiprocessing.dummy import Pool
from multiprocessing import cpu_count




def getTripReports(title, hikeurl, params=None):
    """Accepts a url of the hike, finds all of the subsequent trip reports,
    scrapes them and inserts them into a MongoDB

    **Input parameters**
    ------------------------------------------------------------------------------
    title: string.  Hike name.

    hikeurl: string. Base URL for the request.

    params: dictionary.  Parameters to be included in the request.

    **Output**
    ------------------------------------------------------------------------------
    None. Appends entry to MongoDB using Pymongo
    """
    r = requests.get(hikeurl + '/@@related_tripreport_listing', params).text
    soup = BeautifulSoup(r, 'lxml')
    for d in soup.select('div.item'):
        if d.select('div.show-with-full') == []:
            continue
        elif d.select('div.show-with-full')[0].p == None:
            db.trip_reports.insert_one({'Name': title,
                                        "Creator": d.select('div.CreatorInfo')[0].span.a.text,
                                        "Date": d.select('span.elapsed-time')[0]['title'],
                                        "Text": d.select('div.show-with-full')[0].text
                                        })
        else:
            db.trip_reports.insert_one({'Name': title,
                                        "Creator": d.select('div.CreatorInfo')[0].span.a.text,
                                        "Date": d.select('span.elapsed-time')[0]['title'],
                                        "Text": d.select('div.show-with-full')[0].p.text
                                        })

def iterateTripReports(title, hikeurl):
    """Determines the number of times to call getTripReports function based on
    the number of trip reports listed on the hike homepage.


    **Input parameters**
    ------------------------------------------------------------------------------
    title: string.  Hike name.

    hikeurl: string. Base URL for the request.

    **Output**
    ------------------------------------------------------------------------------
    None. Appends entry to MongoDB using pymongo.
    """
    r = requests.get(hikeurl + '/@@related_tripreport_listing').text
    soup = BeautifulSoup(r, 'lxml')
    numit = math.ceil(float(soup.find('div', {'id': 'count-data'}).text)/5)
    for i in range(int(numit)):
        getTripReports(title, hikeurl, params={'b_start:int': str(i*5)})

def TripReportBuilder(df):
    """Iterates through the rows of loaded pandas dataframe and calls
    iterateTripReports for each hike/row.
    
    **Input parameters**
    ------------------------------------------------------------------------------
    title: pandas dataframe. Dataframe must contain columns entitled 'numReports'
            and 'hike_name'.

    **Output**
    ------------------------------------------------------------------------------
    None. Calls following functions for input of data into MongoDB using Pymongo


    """
    for row in range(len(df)):
        if df['numReports'][row]:
            iterateTripReports(df['hike_name'][row], df['url'][row])
        else:
            continue


if __name__ == '__main__':
    client = MongoClient()
    db = client.wta
    db.trip_reports.drop()
    df = pd.read_csv('data/washington_hikes_clean_noout.csv')
    TripReportBuilder(df)
    print db.trip_reports.count(), ' Trip Reports collected'
