#coding:utf-8
import scrapy
import json
import sys
from scrapy_redis.spiders import RedisCrawlSpider
from MyRedis import get_redis
from scrapy import Request
from CNKI.items import CnkiPageItem
from time import sleep
reload(sys)
sys.setdefaultencoding('utf8')

class CnkiSpider(RedisCrawlSpider):
    name = "CnkiDetailSlave"
    redis_key = 'CnkiDetailSlave:start_urls'
    allowed_domains = ["image.cnki.net"]
    cnki_image_domin = 'http://image.cnki.net/ImageLayout.ashx'
    redis_server = get_redis()

    def parse(self, response=None):
        subject = self.redis_server.lpop('subject')
        if not subject:
            return
        start_page = "1"
        querystring = {
            "sortName": "",
            "keyword": "",
            "showtuzu": "",
            "page": start_page,
            "pagesize": "15",
            "colWidth": "211",
            # "condition": "||||%u4E2D%u533B%u5B66||||||",
            "condition": "||||%s||||||" % self.escape(subject),
        }
        url = self.cnki_image_domin + self.url_cat(querystring)
        yield Request(url, headers=self.headers,
                      callback=self.parse_page, meta={'subject':subject},
                      )


