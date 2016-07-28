import numpy as np
import pandas as pd
import re
import requests


def dropCols(data):
    data.drop(['Unnamed: 0', 'Unnamed: 0.1'], axis=1, inplace=True)
    data.drop(['lat', 'long'], axis=1, inplace=True)


def total_dst(string):
    """Extracts mileage from string and calculates total mileage depending on if
    description says one-way or roundtrip."""

    if str(string) == 'nan':
        return np.nan
    else:
        miles = []
        try:
            for s in string.split():
                miles.append(float(s))
        except:
            miles.append(string)
        if 'roundtrip' in string:
            return miles[0]
        elif 'one-way' in string:
            return miles[0]*2
        else:
            return miles[0]


def num_votes(string):
    '''Extracts number of votes'''
    lst = string.strip('(').split()
    if 'NR' in lst:
        return 'NR'
    else:
        return int(lst[0])


def stars(string):
    '''Extracts number of stars'''
    lst = string.split()
    if 'NR' in lst:
        return 'NR'
    else:
        return float(lst[0])


def latlong(string):
    '''Extracts latitude and longitude from url collected'''
    l = re.split('=|&', string)
    ll = [x for x in l if (l.count(x) > 1) and (len(x) > 2)]
    if not ll:
        return 'NR'
    else:
        return ll[0]

def get_time_drive(string, google_key):
    """Uses the Google API key to return drive time from Seattle."""
    if string == 'NR':
        return 'NR'
    else:
        try:
            url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=Seattle&destinations='+string+'&avoid=tolls&key='+google_key
            resp = requests.get(url)
            if resp.status_code != 200:
                # This means something went wrong.
                break
                raise ApiError('GET /tasks/ {}'.format(resp.status_code))
            else:
                return resp.json()['rows'][0]['elements'][0]['duration']['value']/float(60)
        except:
            return 'NA'


def cleanData(data):
    dropCols(data)
    data['total_dist'] = data['length'].apply(total_dst)
    data['number_votes'] = data['number_votes'].apply(num_votes)
    data['pass(0-no pass, 1- pass required)'] = [0 if 'No pass' in x else 1for x in data['which_pass']]
    data['stars'] = data['rating'].apply(stars)
    data['lat_long'] = data['latlong'].apply(latlong)
    data['time_from_seattle'] = data['lat_long'].apply(get_time_drive)
    data.replace('NA', np.nan, inplace=True)
    data.replace('NR', np.nan, inplace=True)
    data.to_csv('washington_hikes_clean.csv', encoding='utf-8')
