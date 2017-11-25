# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from peewee import *
db = MySQLDatabase("CNKI", host='localhost', user="root", passwd="jiangchuan", charset="utf8")

class CnkiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    img_url = scrapy.Field()
    format_source = scrapy.Field()
    img_path = scrapy.Field()
    source = scrapy.Field()
    keyword = scrapy.Field()
    context = scrapy.Field()


class CnkiPageItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ArticleTitle = scrapy.Field()
    image_height = scrapy.Field()
    image_id = scrapy.Field()
    image_url = scrapy.Field()
    leftside = scrapy.Field()
    longtitle = scrapy.Field()
    patent_nofont = scrapy.Field()
    title = scrapy.Field()
    title_nofont = scrapy.Field()
    url = scrapy.Field()
    width = scrapy.Field()
    subject = scrapy.Field()


class CnkiPage(Model):
    image_id = CharField(max_length=255, primary_key=True)
    ArticleTitle = CharField(max_length=255, null=True)
    image_height = CharField(max_length=255, null=True)
    image_url = TextField(null=False)
    leftside =  CharField(max_length=255, null=True)
    longtitle = CharField(max_length=255, null=True)
    patent_nofont =  CharField(max_length=255, null=True)
    title =  CharField(max_length=255, null=False)
    title_nofont =  CharField(max_length=255, null=True)
    url = TextField(null=False)
    width = CharField(max_length=255, null=True)
    subject = CharField(max_length=255, null=True, default=None)

    class Meta:
        database = db