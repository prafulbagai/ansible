
from boto.s3.key import Key
import os
from boto.s3.connection import S3Connection

AWS_STORAGE_BUCKET_NAME = 'message-icons'
AWS_ACCESS_KEY_ID = 'AKIAJSIFWXF4UOQPMFMQ'
AWS_SECRET_ACCESS_KEY = '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'
AWS_S3_HOST = 's3.ap-south-1.amazonaws.com'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY,
                    host=AWS_S3_HOST)
bucket = conn.get_bucket(AWS_STORAGE_BUCKET_NAME)


def upload_to_s3(file_path, file_name):
    key_info = Key(bucket)
    key_info.key = file_name
    key_info.set_contents_from_filename(file_path)
    bucket.set_acl('public-read', file_name)
    print vars(bucket)
    url = key_info.generate_url(expires_in=0, query_auth=False)
    return url

directory = '/Users/praful/Desktop/cube/c26_mclients/Brand Icons/'
icons = [p for p in os.listdir(directory)]
for icon in icons:
    if not icon.endswith('.png'):
        continue
    file_path = directory + icon
    print upload_to_s3(file_path, '/media/' + icon)
