# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from ..items import WtaScrapersItem


class WtaHikeScraper(scrapy.Spider):
    name = 'hikes'
    allowed_domains = ['wta.org']
    start_urls = ['https://www.wta.org/go-outside/hikes']

    def parse(self, response):
        page_interval = 30
        page_link = 'https://www.wta.org/go-outside/hikes?b_start:int={}'
        last_page = response.xpath("//*[@id='portal-column-content']//div[@class='search-listing']//div[@id='hike_results']//li[@class='last']/a/@href").extract()
        num_pages = int(last_page[-1].split("=")[-1])/page_interval
        pages = [page_link.format(str(page * page_interval)) for page in range(0, int(num_pages+1))]
        for page in pages:
            yield scrapy.Request(page, callback=self.parse_pages, dont_filter=True)
            # thing = scrapy.Request(page, callback=self.parse_pages, dont_filter=True)
            # thing = self.parse_pages(scrapy.Request(page))

    def parse_pages(self, response):
        hike_pages = response.xpath("//*[@id='hike_results']//div[@class='search-result-listing']/a/@href").extract()
        for page in hike_pages:
            yield scrapy.Request(page, callback=self.parse_profiles, dont_filter=True)

    def parse_profiles(self, response):
        l = ItemLoader(item=WtaScrapersItem(), response=response)

        # features
        hike_name = response.xpath("//h1[@class='documentFirstHeading']/text()").extract_first()
        region = response.xpath("//div[@class='hike-stat grid_3 alpha']/div/text()").extract_first()
        if region is None:
            region = response.xpath("//div[@id='hike-region']/span/text()").extract_first()
        distance = response.xpath("//div[@id='distance']/span/text()").extract_first()
        elevation_gain = response.xpath("//div[@class='hike-stat']/div/span/text()").extract_first()
        rating = response.xpath("//div[@class='current-rating']/text()").extract_first()
        number_votes = response.xpath("//div[@class='rating-count']/text()").extract_first()
        features = response.xpath("//div[@id='hike-features']/div/@data-title").extract()
        pass_needed = response.xpath("//div[@class='alerts-and-conditions']/div/a/text()").extract_first()
        description = '\n'.join(response.xpath("//div[@id='hike-body-text']/p/text()").extract())
        latlong = response.xpath("//a[@class='visualNoPrint full-map']/@href").extract_first()
        url = response.url

        l.add_value('HikeName', hike_name)
        l.add_value('Region', region)
        l.add_value('Subregion', region)
        l.add_value('TotalDistance', distance)
        l.add_value('ElevationGain', elevation_gain)
        l.add_value('Description', description)
        l.add_value('PassNeeded', pass_needed)
        l.add_value('LatLong', latlong)
        l.add_value('TimeFromSeattle', latlong)
        l.add_value('Coast', feature_present(features, 'coast'))
        l.add_value('DogsAllowed', feature_present(features, 'Dogs allowed on leash'))
        l.add_value('EstablishedCampsites', feature_present(features, 'established campsites'))
        l.add_value('FallFoliage', feature_present(features, 'fall foliage'))
        l.add_value('GoodForKids', feature_present(features, 'good for kids'))
        l.add_value('Lakes', feature_present(features, 'lakes'))
        l.add_value('MountainViews', feature_present(features, 'Mountain views'))
        l.add_value('OldGrowth', feature_present(features, 'old growth'))
        l.add_value('RidgesPasses', feature_present(features, 'ridges/passes'))
        l.add_value('Rivers', feature_present(features, 'rivers'))
        l.add_value('Summits', feature_present(features, 'summits'))
        l.add_value('Waterfalls', feature_present(features, 'waterfalls'))
        l.add_value('WildflowersMeadows', feature_present(features, 'wildflowers/meadows'))
        l.add_value('Wildlife', feature_present(features, 'wildlife'))
        l.add_value('Url', url)
        l.add_value('Rating', rating)
        l.add_value('NumVotes', number_votes)

        return l.load_item()


def feature_present(features, string):
    features_lower = [f.lower() for f in features]
    return True if string.lower() in features_lower else False