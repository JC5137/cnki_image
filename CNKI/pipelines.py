# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from twisted.enterprise import adbapi
from CNKI.items import CnkiPage



class CnkiPipeline(object):
    def process_item(self, item, spider):
        if CnkiPage.table_exists() == False:
            CnkiPage.create_table()
        CnkiPage.insert(**item).execute()
        return item
