# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from ..items import WtaScrapersItem


class TripReportScraper(scrapy.Spider):
    name = 'hikes'
    allowed_domains = ['wta.org']
    start_urls = ['https://www.wta.org/go-outside/trip-reports']

    def parse(self, response):
        page_interval = 100
        page_link = 'https://www.wta.org/@@search_tripreport_listing?b_size={}&amp;b_start:int={}'
        num_pages = response.xpath("//*[@class='pagination']//li[@class='last']/a/text()").extract_first()
        pages = [page_link.format(str(page_interval), str(n * page_interval)) for n in range(0, int(num_pages)+1)]
        for page in pages:
            yield scrapy.Request(page, callback=self.parse_pages, dont_filter=True)
            # thing = scrapy.Request(page, callback=self.parse_pages, dont_filter=True)
            # thing = self.parse_pages(scrapy.Request(page))

    def parse_pages(self, response):
        hike_pages = response.xpath("//*[@class='item']//a[@class='show-with-full full-report-link visualNoPrint hidden-480 wta-action button']/@href").extract()
        for page in hike_pages:
            yield scrapy.Request(page, callback=self.parse_profiles, dont_filter=True)

    def parse_profiles(self, response):
        l = ItemLoader(item=WtaScrapersItem(), response=response)

        # features
        hike_name = response.xpath("//h1[@class='documentFirstHeading']/a/text()").extract_first()
        author_name = response.xpath("//div[@class='CreatorInfo']/span/a/text()").extract()[1]
        trail_notes = response.xpath("//div[@class='trip-condition']/span/text()").extract()
        trail_conditions = trail_notes[1] if len(trail_notes) > 1 else None
        road = trail_notes[2] if len(trail_notes) > 2 else None
        bugs = trail_notes[3] if len(trail_notes) > 3 else None
        snow = trail_notes[4] if len(trail_notes) > 4 else None
        date_hiked = response.xpath("//div[@class='HikedDate']/span[@class='elapsed-time']/@datetime").extract_first()
        description = '\n'.join(response.xpath("//div[@id='tripreport-body-text']/p/text()").extract())
        url = response.url

        l.add_value('HikeName', hike_name)
        l.add_value('AuthorName', author_name)
        l.add_value('TrailConditions', trail_conditions)
        l.add_value('Road', road)
        l.add_value('Bugs', bugs)
        l.add_value('Snow', snow)
        l.add_value('ReportText', description)
        l.add_value('DateHiked', date_hiked)
        l.add_value('Url', url)

        return l.load_item()
