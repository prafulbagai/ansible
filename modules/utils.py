
import json
import os
import requests

from boto.s3.key import Key
from datetime import datetime
from boto.s3.connection import S3Connection, OrdinaryCallingFormat
from django.conf import settings

epoch = datetime.utcfromtimestamp(0)

os.environ['S3_USE_SIGV4'] = 'True'

conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY,
                    host=settings.AWS_S3_HOST,
                    calling_format=OrdinaryCallingFormat())
bucket = conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)


def get_post_params(request):
    data = request.POST
    if not data:
        try:
            data = json.loads(request.body)
        except:
            data = {}
    return data


def datetime_to_milli(dt):
    dt = dt.replace(tzinfo=None)
    return int((dt - epoch).total_seconds() * 1000)


def milli_to_datetime(ms):
    return datetime.fromtimestamp(ms / 1000.0)


def upload_to_s3(file_path, file_name):
    key_info = Key(bucket)
    key_info.key = file_name
    key_info.set_contents_from_filename(file_path)
    bucket.set_acl('public-read', file_name)
    url = key_info.generate_url(expires_in=0, query_auth=False)
    return url


def download_file_from_url(url, filename=None):
    if not filename:
        filename = 'temp'

    req = requests.get(url)
    with open(filename, 'wb') as fle:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                fle.write(chunk)
    return filename


def is_key_available(keys_posted, *required_args):
    for key in required_args:
        if key not in keys_posted:
            return (False, key)
    return (True, None)


def check_args(cls, *required_args):
    def wrapper(func):
        def inner(self, request, *args, **kwargs):  # inner function needs parameters
            if request.method == 'GET':
                keys_posted = request.GET.keys()
            else:
                keys_posted = get_post_params(request).keys()

            available, key = is_key_available(keys_posted, *required_args)
            if not available:
                response = {
                    'status': 400,
                    'message': 'key `' + str(key) + '` not present'
                }
                return JsonResponse(response, safe=False)
            return func(self, request, *args, **kwargs)
        return inner
    return wrapper
