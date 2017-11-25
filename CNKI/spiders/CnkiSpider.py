#coding:utf-8
import re
import copy
import json
import sys
from scrapy_redis.spiders import RedisCrawlSpider
from MyRedis import get_redis
from scrapy import Request
from CNKI.items import CnkiPageItem
from CNKI.utils.string_process import deescape
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

    def parse(self, response):
        result = json.loads(response.body)
        is_success = result['success']
        end_page = int(result['pages'])
        current_page = int(result['page'])
        subject_escape = re.findall('(?<=condition=).*?(?=$)', response.url)[0]
        subject = deescape(subject_escape)

        # TODO: 断点续爬
        if not result['data']:
            # 反爬，需要暂停一段时间，链接导入到redis
            sleep(60 * 10)
            self.redis_server.lpush(self.name + ':' + 'block_url', response.url)
        else:
            for c_item in result['data']:
                item = CnkiPageItem()
                for key in c_item:
                    item[key] = c_item[key]
                item['subject'] = subject
                self.redis_server.lpush('CnkiDetailSlave:start_urls', item['url'])
                yield item

        if current_page < end_page:
            next_page = current_page + 1
            url = response.url.replace('&page=%d' % current_page, '&page=%d' % next_page)
            yield Request(url,callback=self.parse)

