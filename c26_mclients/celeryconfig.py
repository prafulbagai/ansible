
from django.conf import settings


CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
if settings.DEBUG:
    BROKER_URL = 'amqp://guest:guest@localhost//'
else:
    BROKER_URL = 'amqp://admin:17576cube@localhost:5672/myvhost/'

CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
CELERY_IMPORTS = ('modules.groups.tasks',)
