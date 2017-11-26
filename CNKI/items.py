# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from peewee import *
from playhouse.pool import PooledMySQLDatabase
db = PooledMySQLDatabase(
    "CNKI",
    max_connections=100,
    stale_timeout=28800,
    user='root',
    host='localhost',
    passwd='jiangchuan',
    charset="utf8",
)
#db = MySQLDatabase("CNKI", host='localhost', user="root", passwd="jiangchuan", charset="utf8")

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


class CnkiImageDetail(scrapy.Item):
    image_id = scrapy.Field()
    key_word = scrapy.Field()
    source = scrapy.Field()
    context = scrapy.Field()
    subject = scrapy.Field()

class ImageItem(scrapy.Item):
    image_path = scrapy.Field()
    image_id = scrapy.Field()

class CnkiImage(Model):
    image_id = CharField(max_length=255, primary_key=True)
    ArticleTitle = TextField(null=False)
    image_height = CharField(max_length=255, null=True)
    image_url = TextField(null=False)
    leftside =  CharField(max_length=255, null=True)
    longtitle = TextField(null=False)
    patent_nofont =  TextField(null=False)
    title =  TextField(null=False)
    title_nofont =  TextField(null=False)
    url = TextField(null=False)
    width = CharField(max_length=255, null=True)
    subject = CharField(max_length=255, null=False)

    image_path = TextField(null=True, default='')
    key_word = CharField(max_length=255, null=True, default='')
    source = TextField(null=True, default='')
    context = TextField(null=True, default='')

    class Meta:
        database = db