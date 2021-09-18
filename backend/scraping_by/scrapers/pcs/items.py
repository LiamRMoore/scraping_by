# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# from itemloaders.processors import TakeFirst, MapCompose


class PcsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class VLOrthoItem(scrapy.Item):
    pass
    # define the fields for your item here like:
    # dataset = scrapy.Field(output_processor=TakeFirst())
    # filesize = scrapy.Field(input_processor=extract_size,#MapCompose(extract_size),
    #                         output_processor=TakeFirst()
    #                         )
    # filename = scrapy.Field(output_processor=TakeFirst())
    # download_url = scrapy.Field(output_processor=TakeFirst())
    # page_url = scrapy.Field(output_processor=TakeFirst())
    # type = scrapy.Field(output_processor=TakeFirst())
    # scale  = scrapy.Field(output_processor=TakeFirst(),
    #                       input_processor=MapCompose(infer_resolution))
    # season = scrapy.Field(output_processor=TakeFirst(),
    #                       input_processor=MapCompose(extract_season))
    # period = scrapy.Field(output_processor=TakeFirst(),
    #                       input_processor=MapCompose((lambda x : x.strip())))
    # region = scrapy.Field(output_processor=TakeFirst(),
    #                       input_processor=MapCompose((lambda x : x.strip())))
    # suffix = scrapy.Field(output_processor=TakeFirst(),
    #                       input_processor=MapCompose(extract_suffix))
