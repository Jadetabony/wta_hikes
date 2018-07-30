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
    Coast = scrapy.Field()
    DogsAllowed = scrapy.Field()
    EstablishedCampsites = scrapy.Field()
    FallFoliage = scrapy.Field()
    GoodForKids = scrapy.Field()
    Lakes = scrapy.Field()
    MountainViews = scrapy.Field()
    OldGrowth = scrapy.Field()
    RidgesPasses = scrapy.Field()
    Rivers = scrapy.Field()
    Summits = scrapy.Field()
    Waterfalls = scrapy.Field()
    WildflowersMeadows = scrapy.Field()
    Wildlife = scrapy.Field()
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
    CreateDate = scrapy.Field(input_processor=MapCompose(lambda x: x.lstrip().rstrip()),
                             output_processor=Join())
    ReviewText = scrapy.Field(input_processor=MapCompose(lambda x: x.lstrip().rstrip()),
                                output_processor=Join())

    # Authors
    MemberSince = scrapy.Field(input_processor=MapCompose(lambda x: x.lstrip().rstrip()),
                          output_processor=Join())
    Name = scrapy.Field(input_processor=MapCompose(lambda x: x.lstrip().rstrip()),
                           output_processor=Join())
