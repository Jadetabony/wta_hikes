import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from pymongo import MongoClient

def scrapeInsertTR(url, name):
    """Requests url, scrapes, finds text and rating, and inserts both into MongoDB.

    **Input parameters**
    ------------------------------------------------------------------------------
    url: string.  Valid url to be requested.  This code is specifically built for
            'http://www.everytrail.com'

    name: string. Name of the hike, scraped from parent function

    **Output**
    ------------------------------------------------------------------------------
    None
    """
    r = requests.get(url).text
    soup = BeautifulSoup(r, 'html.parser')
    if len(soup(attrs={'class': 'comment-content rounded floatright'})):
        for div in soup(attrs={'class': 'comment-content rounded floatright'}):
            rating = div(attrs={'itemprop': "reviewRating"})[0].span['title']
            text = div.p.text
            if len(text):
                db.trainingTR.insert_one({'Name': name,
                                        "Rating": rating,
                                        "Text": text
                                        })
    else:
        for div in soup(attrs={'style': 'overflow:hidden'}):
            if (div.span is None) or div.select('img') == []:
                continue
            else:
                rating = div.select('img')[0]['title'][0]
                text = div.span.text.strip()
                if len(text):
                    db.trainingTR.insert_one({'Name': name,
                                            "Rating": rating,
                                            "Text": text
                                            })


def URLfinder(baseurl):
    """Finds all trailing URLs for hikes.  Calls scrapeInsertTR for all trailing urls.

    **Input parameters**
    ------------------------------------------------------------------------------
    baseurl: string. Valid url to be requested.  This code is specifically built for
            'http://www.everytrail.com/best/hiking-california'

    **Output**
    ------------------------------------------------------------------------------
    None
    """
    r = requests.get(baseurl).text
    soup = BeautifulSoup(r, 'html.parser')
    for div in soup.select('div.guide-preview-content'):
        url = 'http://www.everytrail.com'+div.span.a['href']
        scrapeInsertTR(url, div.span.a.text)


if __name__ == '__main__':
    client = MongoClient()
    db = client.wta
    db.trainingTR.drop()
    URLfinder('http://www.everytrail.com/best/hiking-california')
    URLfinder('http://www.everytrail.com/best/hiking-utah')
    URLfinder('http://www.everytrail.com/best/hiking-oregon')
    URLfinder('http://www.everytrail.com/best/hiking-idaho')
    URLfinder('http://www.everytrail.com/best/hiking-washington')
    print db.trainingTR.count(), ' Trip Reports collected'
