
from django.conf import settings

REDIS_SETTINGS = {
    'host': '127.0.0.1',
    'port': 6379,
    'password': '',
}
if not settings.DEBUG:
    REDIS_SETTINGS['password'] = '17576cube'

GROUP_REDIS_KEY = 'groups'
GROUP_CODE_REDIS_KEY = 'codes'
