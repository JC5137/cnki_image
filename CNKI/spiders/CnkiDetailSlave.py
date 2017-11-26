#coding:utf-8
import re
import os
import sys
import logging
from scrapy_redis.spiders import RedisCrawlSpider
from MyRedis import get_redis
from scrapy import Request
from CNKI.items import CnkiImageDetail, ImageItem
reload(sys)
sys.setdefaultencoding('utf8')

class CnkiSpider(RedisCrawlSpider):
    name = "CnkiDetailSlave"
    redis_key = 'CnkiDetailSlave:start_urls'
    allowed_domains = ["image.cnki.net"]
    cnki_image_domin = 'http://image.cnki.net/ImageLayout.ashx'
    redis_server = get_redis()
    log = logging.getLogger("CnkiDetailSlave")

    def parse(self, response):
        try:
            if 'http://image.cnki.net/detail/' in response.url:
                image_id = response.url.split('/')[-1].split('.')[0]
                context = response.xpath("//meta[@name='description']/@content").extract_first()
                key_word = response.xpath("//meta[@name='keywords']/@content").extract_first()
                source_nofont = response.xpath("//li[@class='detext01']/text()").extract()
                source_font = response.xpath("//li[@class='detext01']/font/text()").extract()
                source_list = [re.sub('\r\n.*?$', '' , s) for s in source_font + source_nofont if re.sub('\r\n.*?$', '' , s) != '']
                source = '##'.join(source_list)
                image_url = "http://image.cnki.net/tempfile/" + image_id + '_w.jpg'
                subject = response.xpath("//table[@class='detext_l'][2]/tbody/tr[last()]/td[last()]/a[@class='blue1']/text()").extract()
                subject = ';'.join(subject)

                item = CnkiImageDetail()
                item['image_id'] = image_id
                item['context'] = context
                item['source'] = source
                item['key_word'] = key_word
                item['subject'] = subject
                yield item

                yield Request(url=image_url, callback=self.parse_image)
        except Exception, err:
            self.log.error(str(err))
            self.log.error(response.url)

    def parse_image(self, response):
        if 'http://image.cnki.net/tempfile/' in response.url:
            image_id = response.url.split('/')[-1].split('_')[0]
            dir_path = 'image'
            image_path = os.path.join(dir_path, image_id +'.jpg')
            with open(image_path, 'wb') as fw:
                fw.write(response.body)
            item = ImageItem()
            item['image_id'] = image_id
            item['image_path'] = image_path
            yield item









