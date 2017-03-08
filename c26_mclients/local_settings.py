
from django.conf import settings

REDIS_SETTINGS = {
    'host': '127.0.0.1',
    'port': 6379,
    'password': '',
}
if not settings.DEBUG:
    REDIS_SETTINGS['password'] = ''

# REDIS KEYS.
GROUP_REDIS_KEY = 'groups'
GROUP_CODE_REDIS_KEY = 'codes'

# JSON KEY.
GROUP_CODES_JSON_KEY = 'group_codes'

# ZIP ICON FOLDER NAME
ICON_FOLDER_NAME = 'Brand Icons'
