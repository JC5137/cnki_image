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

from scrapy_redis.dupefilter import RFPDupeFilter

class CnkiSpider(RedisCrawlSpider):
    name = "CnkiSpider"
    redis_key = 'CnkiSpider:start_urls'
    allowed_domains = ["image.cnki.net"]
    cnki_image_domin = 'http://image.cnki.net/ImageLayout.ashx'
    redis_server = get_redis()

    def escape(self, subject):
        sub = json.dumps(subject).replace('"', '')
        sublist = ['%u' + s.upper() for s in sub.split('\\u') if s != '']
        return ''.join(sublist)

    def url_cat(self, querystring):
        url = '?'
        url_query = [q + '=' + querystring[q] for q in querystring]
        url += '&'.join(url_query)
        return url

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


    def parse_page(self, response):
        subject = response.meta.get('subject')
        result = json.loads(response.body)
        is_success = result['success']
        end_page = int(result['pages'])
        current_page = int(result['page'])

        querystring = {
            "sortName": "",
            "keyword": "",
            "showtuzu": "",
            "page": str(current_page + 1),
            "pagesize": "15",
            "colWidth": "211",
            "condition": "||||%s||||||" % self.escape(subject),
        }

        #TODO: 断点续爬
        for c_item in result['data']:
            # 反爬，需要暂停一段时间，链接导入到redis
            if not c_item:
                sleep(60 * 10)
                self.redis_server.lpush(self.name + ':' + 'block_url', response.url)
            item = CnkiPageItem()
            for key in c_item:
                item[key] = c_item[key]
            item['subject'] = subject
            yield item

        if current_page < end_page:
            yield Request(self.cnki_image_domin + self.url_cat(querystring),
                          headers=self.headers,
                          callback=self.parse_page, meta={'subject': subject},
                          )

        else:
            ##结束此学科的爬取
            yield self.parse()

