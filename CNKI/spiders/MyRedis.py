#coding:utf-8
from scrapy.conf import settings
import redis

def get_redis():
    redis_args = dict(
        host=settings['MYREDIS_HOST'],
        port=settings['MYREDIS_PORT'],
        password=settings["MYREDIS_PASSWORD"]
    )
    return redis.Redis(**redis_args)
        
if __name__ == '__main__':
    my_redis = get_redis()
    print my_redis.keys()
    my_redis.lpush("CnkiSpider:start_urls","http://image.cnki.net/")
    my_redis.lpush("subject", u"外科学")

    
