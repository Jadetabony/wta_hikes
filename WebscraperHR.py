"""Code to scrape trip reports.  Saves code to MongoDB, parses out hike name, username, date and description"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import matplotlib as plt
import seaborn as sn
import re

data = pd.read_csv('data/washington_hikes_clean.csv')
urls = data.url

def get_urls(path):
    r = requests.get(path)
    soup = BeautifulSoup(r.text, 'lxml')
    urls = []
    for div in soup.findAll('div', attrs={"class": "col nine"}):
        print div
        urls.append(div.a.href)
    return urls



if __name__ == "__main__":
    print urls[0]

    print get_urls(urls[0])
