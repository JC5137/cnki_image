# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from twisted.enterprise import adbapi
from CNKI.items import CnkiImage, db

class CnkiPipeline(object):
    def process_item(self, item, spider):
        with db.execution_context():
            if CnkiImage.table_exists() == False:
                CnkiImage.create_table()
            try:
                info_dict = {}
                for k, v in item.items():
                    if k != 'image_id' and v != u'':
                        info_dict[k] = v
                cnki_image = CnkiImage.get(CnkiImage.image_id == item['image_id'])
                CnkiImage.update(**info_dict).where(CnkiImage.image_id == item['image_id']).execute()
            except CnkiImage.DoesNotExist:
                info_dict = {}
                for k, v in item.items():
                    if v != u'':
                        info_dict[k] = v
                CnkiImage.insert(**info_dict).execute()
        return item
