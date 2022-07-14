# -*- coding: utf-8 -*-

"""

Redis Connect function:

"""

import redis
from django.conf import settings


def redis_conf(conf):
    dit={
        'host': conf.get('HOST', 'localhost'),
        'port': conf.get('PORT', 6379),
        'password': conf.get('PASSWORD', ''),
        'db': conf.get('db', 0),
    }
    return dit

conf =redis_conf(settings.REDIS.get('default', {}))
r = redis.StrictRedis(host=conf['host'], port=conf['port'], password=conf['password'],db=conf['db'])
