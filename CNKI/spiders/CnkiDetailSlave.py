#coding:utf-8
import codecs
import re
import os
import sys
from scrapy_redis.spiders import RedisCrawlSpider
from MyRedis import get_redis
from scrapy import Request
from CNKI.items import CnkiImageItem, ImageItem
reload(sys)
sys.setdefaultencoding('utf8')

class CnkiSpider(RedisCrawlSpider):
    name = "CnkiDetailSlave"
    redis_key = 'CnkiDetailSlave:start_urls'
    allowed_domains = ["image.cnki.net"]
    cnki_image_domin = 'http://image.cnki.net/ImageLayout.ashx'
    redis_server = get_redis()

    def parse(self, response):
        try:
            if 'http://image.cnki.net/detail/' in response.url:
                image_id = response.url.split('/')[-1].split('.')[0]
                context = response.xpath("//meta[@name='description']/@content").extract()[0]
                key_word = response.xpath("//meta[@name='keywords']/@content").extract()[0]
                source_nofont = response.xpath("//li[@class='detext01']/text()").extract()
                source_font = response.xpath("//li[@class='detext01']/font/text()").extract()
                source_list = [re.sub('\r\n.*?$', '' , s) for s in source_font + source_nofont if re.sub('\r\n.*?$', '' , s) != '']
                source = '##'.join(source_list)
                image_url = response.xpath("//img[@id='cnkiimage']/@src").extract()[0]
                subject = response.xpath("//table[@class='detext_l'][2]/tbody/tr[last()]/td[last()]/a[@class='blue1']/text()").extract()[0]

                item = CnkiImageItem()
                item['image_id'] = image_id
                item['context'] = context
                item['source'] = source
                item['key_word'] = key_word
                yield item

                yield Request(url=image_url, callback=self.parse_image, meta={'subject': subject})
        except Exception, err:
            print str(err)
            print response.url

    def parse_image(self, response):
        if 'http://image.cnki.net/tempfile/' in response.url:
            image_id = response.url.split('/')[-1].split('_')[0]
            subject = response.meta['subject']
            dir_path = os.path.join('image', subject)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            image_path = os.path.join(dir_path, image_id +'.jpg')
            with open(image_path, 'wb') as fw:
                fw.write(response.body)
            item = ImageItem()
            item['image_id'] = image_id
            item['image_path'] = image_path
            yield item









