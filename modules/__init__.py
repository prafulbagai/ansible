
import redis

from django.conf import settings

REDIS_CLIENT = redis.StrictRedis(**settings.REDIS_SETTINGS)
