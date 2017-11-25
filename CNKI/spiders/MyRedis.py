#coding:utf-8
from scrapy.conf import settings
import copy
import redis
from CNKI.utils.string_process import *

def get_redis():
    redis_args = dict(
        host=settings['MYREDIS_HOST'],
        port=settings['MYREDIS_PORT'],
        password=settings["MYREDIS_PASSWORD"]
    )
    return redis.Redis(**redis_args)
        
if __name__ == '__main__':
    my_redis = get_redis()
    page = 1
    query_s = copy.deepcopy(querystring)
    subject = [
        '外科学',
        '肿瘤学',
        '中医学',
    ]
    cnki_image_domin = 'http://image.cnki.net/ImageLayout.ashx'
    for s in subject:
        query_s['condition'] = escape(s)
        query_s['page'] = str(page)
        url = cnki_image_domin + url_cat(query_s)
        my_redis.lpush("CnkiSpider:start_urls", url)

    
