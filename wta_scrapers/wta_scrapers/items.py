# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, Join


class WtaScrapersItem(scrapy.Item):
    HikeName = scrapy.Field(input_processor=MapCompose(lambda x: x.lstrip().rstrip()),
                           output_processor=Join())
    Region = scrapy.Field(input_processor=MapCompose(lambda x: x.lstrip().rstrip()),
                            output_processor=Join())
    Subregion = scrapy.Field(input_processor=MapCompose(lambda x: x.lstrip().rstrip()),
                          output_processor=Join())
    TotalDistance = scrapy.Field(input_processor=MapCompose(lambda x: x.lstrip().rstrip()),
                          output_processor=Join())
    LatLong = scrapy.Field(input_processor=MapCompose(lambda x: x.lstrip().rstrip()),
                                 output_processor=Join())
    ElevationGain = scrapy.Field(input_processor=MapCompose(lambda x: x.lstrip().rstrip()),
                               output_processor=Join())
    TimeFromSeattle = scrapy.Field(input_processor=MapCompose(lambda x: x.lstrip().rstrip()),
                          output_processor=Join())
    Coast = scrapy.Field(output_processor=Join())
    DogsAllowed = scrapy.Field(output_processor=Join())
    EstablishedCampsites = scrapy.Field(output_processor=Join())
    FallFoliage = scrapy.Field(output_processor=Join())
    GoodForKids = scrapy.Field(output_processor=Join())
    Lakes = scrapy.Field(output_processor=Join())
    MountainViews = scrapy.Field(output_processor=Join())
    OldGrowth = scrapy.Field(output_processor=Join())
    RidgesPasses = scrapy.Field(output_processor=Join())
    Rivers = scrapy.Field(output_processor=Join())
    Summits = scrapy.Field(output_processor=Join())
    Waterfalls = scrapy.Field(output_processor=Join())
    WildflowersMeadows = scrapy.Field(output_processor=Join())
    Wildlife = scrapy.Field(output_processor=Join())
    Url = scrapy.Field(input_processor=MapCompose(lambda x: x.lstrip().rstrip()),
                          output_processor=Join())
    Rating = scrapy.Field(input_processor=MapCompose(lambda x: x.lstrip().rstrip()),
                              output_processor=Join())
    NumVotes = scrapy.Field(input_processor=MapCompose(lambda x: x.lstrip().rstrip()),
                          output_processor=Join())
    Description = scrapy.Field(input_processor=MapCompose(lambda x: x.lstrip().rstrip()),
                          output_processor=Join())
    PassNeeded = scrapy.Field(input_processor=MapCompose(lambda x: x.lstrip().rstrip()),
                          output_processor=Join())

    # trip reports
    DateHiked = scrapy.Field(input_processor=MapCompose(lambda x: x.lstrip().rstrip()),
                             output_processor=Join())
    ReportText = scrapy.Field(input_processor=MapCompose(lambda x: x.lstrip().rstrip()),
                                output_processor=Join())
    TrailConditions = scrapy.Field(input_processor=MapCompose(lambda x: x.lstrip().rstrip()),
                                output_processor=Join())
    Road = scrapy.Field(input_processor=MapCompose(lambda x: x.lstrip().rstrip()),
                              output_processor=Join())
    Bugs = scrapy.Field(input_processor=MapCompose(lambda x: x.lstrip().rstrip()),
                              output_processor=Join())
    Snow = scrapy.Field(input_processor=MapCompose(lambda x: x.lstrip().rstrip()),
                                   output_processor=Join())

    # Authors
    MemberSince = scrapy.Field(input_processor=MapCompose(lambda x: x.lstrip().rstrip()),
                          output_processor=Join())
    AuthorName = scrapy.Field(input_processor=MapCompose(lambda x: x.lstrip().rstrip()),
                           output_processor=Join())
