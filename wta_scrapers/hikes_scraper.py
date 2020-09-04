# -*- coding: utf-8 -*-
import requests
from lxml import html
from collections import OrderedDict


class WtaHikeScraper(object):

    def __init__(self):
        self.name = 'hikes'
        self.page_interval = 30
        self.start_page = 'https://www.wta.org/go-outside/hikes'
        self.data_file = '../data/wta_hike_data_20200820.tsv'

    def parse_and_write(self):
        tree = self.get_html_tree(self.start_page)
        page_link = 'https://www.wta.org/go-outside/hikes?b_start:int={}'
        last_page = tree.xpath("//*[@id='portal-column-content']//div[@class='search-listing']//div[@id='hike_results']//li[@class='last']/a/@href")
        num_pages = int(last_page[-1].split("=")[-1])/self.page_interval
        pages = [page_link.format(str(page * self.page_interval)) for page in range(0, int(num_pages+1))]
        headers = False
        counter = 0
        num_hikes = num_pages * 30
        with open(self.data_file, 'w') as df:
            for landpage in pages:
                response = self.get_html_tree(landpage)
                hike_pages = self.parse_pages(response)
                for page in hike_pages:
                    print('Scraped {} hikes of {}\r'.format(counter, num_hikes))
                    response = self.get_html_tree(page)
                    try:
                        hike_info = self.parse_profiles(response, page)
                        if headers is False:
                            heads = '\t'.join(hike_info.keys())
                            df.write('{}\n'.format(heads))
                            headers = True
                        vals = '\t'.join(hike_info.values())
                        df.write('{}\n'.format(vals))
                        counter += 1
                    except:
                        print("Skipping 1")
                        continue

    @staticmethod
    def get_html_tree(page):
        response = requests.get(page)
        tree = html.fromstring(response.content)
        return tree

    @staticmethod
    def parse_pages(response):
        hike_pages = response.xpath("//*[@id='hike_results']/div/div/div/div/a/@href")
        return hike_pages

    @staticmethod
    def parse_profiles(response, page):
        l = OrderedDict()
        
        # features
        hike_name = response.xpath("//h1[@class='documentFirstHeading']/text()")
        region = response.xpath("//div[@class='hike-stat grid_3 alpha']/div/text()")
        if len(region) == 0:
            region = response.xpath("//div[@id='hike-region']/span/text()")
        distance = response.xpath("//div[@id='distance']/span/text()")
        elevation_gain = response.xpath("//div[@class='hike-stat']/div/span/text()")
        rating = response.xpath("//div[@class='current-rating']/text()")
        number_votes = response.xpath("//div[@class='rating-count']/text()")
        features = response.xpath("//div[@id='hike-features']/div/@data-title")
        pass_needed = response.xpath("//div[@class='alerts-and-conditions']/div/a/text()")
        description = ' '.join([r.strip().lstrip() for r in response.xpath("//div[@id='hike-body-text']/p/text()")])
        latlong = response.xpath("//a[@class='visualNoPrint full-map']/@href")
        trip_reports_list = response.xpath("//span[@class='ReportCount']/text()")
        count_tripreports = 0
        if len(trip_reports_list) > 0:
            count_tripreports = trip_reports_list[0]

        l['HikeName'] = hike_name[0]
        l['Region'] = region[0] if region else 'None'
        l['Subregion'] = region[0] if region else 'None'
        l['TotalDistance'] = ' '.join(distance) if distance else 'None'
        l['ElevationGain'] = elevation_gain[0] if elevation_gain else 'None'
        l['Description'] = description
        l['PassNeeded'] = pass_needed[0] if pass_needed else 'None'
        l['LatLong'] = latlong[0] if latlong else 'None'
        l['TimeFromSeattle'] = latlong[0] if latlong else 'None'
        l['Coast'] = feature_present(features, 'coast')
        l['DogsAllowed'] = feature_present(features, 'Dogs allowed on leash')
        l['EstablishedCampsites'] = feature_present(features, 'established campsites')
        l['FallFoliage'] = feature_present(features, 'fall foliage')
        l['GoodForKids'] = feature_present(features, 'good for kids')
        l['Lakes'] = feature_present(features, 'lakes')
        l['MountainViews'] = feature_present(features, 'Mountain views')
        l['OldGrowth'] = feature_present(features, 'old growth')
        l['RidgesPasses'] = feature_present(features, 'ridges/passes')
        l['Rivers'] = feature_present(features, 'rivers')
        l['Summits'] = feature_present(features, 'summits')
        l['Waterfalls'] = feature_present(features, 'waterfalls')
        l['WildflowersMeadows'] = feature_present(features, 'wildflowers/meadows')
        l['Wildlife'] = feature_present(features, 'wildlife')
        l['Url'] = page
        l['Rating'] = rating[0].split()[0] if rating else 'None'
        l['NumVotes'] = number_votes[0].split()[0].replace('(', '') if number_votes else 'None'
        l['countTripReports'] = count_tripreports
        return l


def feature_present(features, string):
    features_lower = [f.lower() for f in features]
    return '1' if string.lower() in features_lower else '0'


if __name__ == "__main__":
    print('Running scraper')
    scraper = WtaHikeScraper()
    scraper.parse_and_write()
