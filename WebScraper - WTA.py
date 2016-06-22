"""Code to scrape text off of WTA website"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import matplotlib as plt
import seaborn as sn
import re

data = pd.read_csv('washington_hikes.csv')


def collect_hikeurls(starturl):
    """Collecting all of the websites for all of the hikes"""
    hike_links = []
    path = starturl
    counter = 0
    while True:
        r = requests.get(path)
        soup = BeautifulSoup(r.text, 'lxml')
        for div in soup.findAll('a', attrs={'class': 'listitem-title'}):
            hike_links.append(div['href'])
            counter += 1
        print 'Collected %d websites' % counter
        link = soup.find('span', attrs={'class': 'next'})
        if link is None:
            break
        else:
            path = link.a['href']
    return hike_links

urls = collect_hikeurls('http://www.wta.org/go-hiking/hikes')


def parser(url):
    """Parses URL into hiking dataset.

    Parser collects html soup and populates
    washington_hikes table with relevant data. Data cleaning is completed in a
    seperate python script."""

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    row_data = {}
    row_data['hike_name'] = soup.find('h1', attrs={'class': "documentFirstHeading"}).text.strip()
    try:
        row_data['region'] = soup.find('div', attrs={'class': "hike-stat grid_3 alpha"}).div.text.strip()
    except:
        try:
            row_data['region'] = soup.find('div', attrs={'id': 'hike-region'}).span.text
        except:
            row_data['region'] = 'NR'
    try:
        lengain = []
        for div in soup.findAll('div', attrs={'class': "hike-stat grid_3"}):
            lengain.append(div.div.span.text)
        row_data['length'] = lengain[0]
        row_data['elevation gain'] = lengain[1]
    except:
        row_data['length'] = 'NR'
        row_data['elevation gain'] = 'NR'
    try:
        row_data['rating'] = soup.find('div', attrs={'class': "current-rating"}).text
    except:
        row_data['rating'] = 'NR'
    try:
        row_data['number_votes'] = soup.find('div', attrs={'class': "rating-count"}).text
    except:
        row_data['number_votes'] = 'NR'
    try:
        features = []
        for div in soup.findAll('div', attrs={'class': "feature grid_1 "}):
            features.append(div['data-title'])
        row_data['features'] = features
    except:
        row_data['features'] = 'NR'
    try:
        row_data['which_pass'] = soup.find('div', attrs={'id': "pass-required-info"}).a.text
    except:
        row_data['which_pass'] = 'NR'
    try:
        row_data['latlong'] = soup.find('a', attrs={'class': "visualNoPrint full-map"})['href']
    except:
        row_data['latlong'] = 'NR'
    try:
        row_data['numReports'] = soup.find('span', attrs={'class': 'ReportCount'}).text
    except:
        row_data['numReports'] = 'NR'
    row_data['url'] = url
    return row_data


def build_dataset(data, urls):
    """Adds parsed fields to dataset.

    Runs though links in urls and applies parser function to the soup Collected
    from the link.  Saves to csv every 50 querries.

    data: dataset to append data to

    urls: List of urls"""
    cnter = 0
    row = -1
    for lnk in urls:
        row += 1
        d = parser(lnk)
        for key in d.keys():
            data.set_value(row, key, d[key])
        cnter += 1
        if cnter % 50 == 0:
            data.to_csv('washington_hikes.csv', encoding='utf-8')
            print 'Saving ', cnter
    data.to_csv('washington_hikes.csv', encoding='utf-8')


def getting_hike_desc(url):
    """Collects hike description from url."""
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    try:
        return soup.find('div', attrs={'id': 'hike-body-text'}).p.text
    except:
        return None



def addtodf(data, row=-1, counter=0):
    """Collects hike description by row of a dataframe.

    Keeps track of number of descriptions collected.
    Can specify starting row in hyperparameters.

    data: dataset to add description to

    row: row to start on

    counter: counter to keep track of descriptions collected"""
    for url in data['url']:
        row += 1
        data.set_value(row, 'hike_desc', getting_hike_desc(data['url'][row]))
        counter += 1
        if counter % 50 == 0:
            data.to_csv('washington_hikes.csv', encoding='utf-8')
            print 'Collected %d hike descriptions' % counter
    data.to_csv('washington_hikes.csv', encoding='utf-8')


if __name__ == '__main__':
    urls = collect_hikeurls('http://www.wta.org/go-hiking/hikes')
    data = pd.read_csv('washington_hikes.csv')
    build_dataset(data, urls)
    addtodf(data)
