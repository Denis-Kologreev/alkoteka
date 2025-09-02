# alkoteka_parser/items.py

import scrapy
from datetime import datetime
from scrapy.loader.processors import TakeFirst, MapCompose, Join


def parse_price(value):
    return float(value.replace(' ', '').replace('₽', '')) if value else 0.0


def get_discount(current, original):
    if current and original and current < original:
        discount = round((original - current) / original * 100)
        return f"Скидка {discount}%"
    return None


class AlkotekaItem(scrapy.Item):
    timestamp = scrapy.Field(serializer=int)
    RPC = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    marketing_tags = scrapy.Field(serializer=list)
    brand = scrapy.Field()
    section = scrapy.Field(serializer=list)
    price_data = scrapy.Field()
    stock = scrapy.Field()
    assets = scrapy.Field()
    metadata = scrapy.Field()
    variants = scrapy.Field(serializer=int)

    def __init__(self, *args, **kwargs):
        super(AlkotekaItem, self).__init__(*args, **kwargs)
        self['timestamp'] = int(datetime.now().timestamp())
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AlkotekaParserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
