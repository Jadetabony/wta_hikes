# -*- coding: utf-8 -*-
import requests
from lxml import html
from collections import OrderedDict
from selenium import webdriver
import time

class TripReportScraper(object):

    def __init__(self):
        self.name = 'trip_reports'
        self.page_interval = 100
        self.start_page = 'https://www.wta.org/go-outside/trip-reports'
        self.data_file = '../data/trip_report_data.tsv'
        
    @staticmethod
    def get_html_tree(page):
        response = requests.get(page)
        tree = html.fromstring(response.content)
        return tree

    def parse_and_write(self):
        browser = webdriver.Chrome()
        browser.get(self.start_page)
        time.sleep(5)
        num_pages = browser.find_element_by_xpath("//*[@class='pagination']//li[@class='last']/a").get_attribute('text')
        page_link = 'https://www.wta.org/@@search_tripreport_listing?b_size={}&amp;b_start:int={}'
        pages = [page_link.format(str(self.page_interval), str(n * self.page_interval)) for n in range(0, int(num_pages)+1)]
        headers = False
        counter = 0
        num_hikes = int(num_pages) * self.page_interval
        with open(self.data_file, 'w') as df:
            for landpage in pages:
                response = self.get_html_tree(landpage)
                hike_pages = self.parse_pages(response)
                for page in hike_pages:
                    print('Scraped {} hikes of {}\r'.format(counter, num_hikes))
                    response = self.get_html_tree(page)
                    hike_info = self.parse_profiles(response, page)
                    if headers is False:
                        heads = '\t'.join(hike_info.keys())
                        df.write('{}\n'.format(heads))
                        headers = True
                    vals = '\t'.join(hike_info.values())
                    df.write('{}\n'.format(vals))
                    counter += 1

    def parse_pages(self, response):
        hike_pages = response.xpath("//*[@class='item']//a[@class='show-with-full full-report-link visualNoPrint hidden-480 wta-action button']/@href")
        return hike_pages

    def parse_profiles(self, response, page):
        l = OrderedDict()

        # features
        hike_name = response.xpath("//h1[@class='documentFirstHeading']/a/text()")
        author_name = response.xpath("//div[@class='CreatorInfo']/span/a/text()")
        trail_notes = response.xpath("//div[@class='trip-condition']/span/text()")
        trail_conditions = trail_notes[1] if len(trail_notes) > 1 else None
        road = trail_notes[2] if len(trail_notes) > 2 else None
        bugs = trail_notes[3] if len(trail_notes) > 3 else None
        snow = trail_notes[4] if len(trail_notes) > 4 else None
        date_hiked = response.xpath("//div[@class='HikedDate']/span[@class='elapsed-time']/@datetime")
        description = ' '.join(response.xpath("//div[@id='tripreport-body-text']/p/text()"))

        l['HikeName'] = hike_name[0] if hike_name else 'None'
        l['AuthorName'] = author_name[1] if author_name else 'None'
        l['TrailConditions'] = trail_conditions
        l['Road'] = road
        l['Bugs'] = bugs
        l['Snow'] = snow
        l['ReportText'] = description
        l['DateHiked'] = date_hiked[0] if date_hiked else 'None'
        l['Url'] = page

        return l


if __name__ == "__main__":
    print('Running Trip Report scraper')
    scraper = TripReportScraper()
    scraper.parse_and_write()
