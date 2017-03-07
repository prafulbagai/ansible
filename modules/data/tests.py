
from boto.s3.key import Key
from boto.s3.connection import S3Connection, OrdinaryCallingFormat

AWS_STORAGE_BUCKET_NAME = 'delivered.reosapps.com'
AWS_ACCESS_KEY_ID = 'AKIAJSIFWXF4UOQPMFMQ'
AWS_SECRET_ACCESS_KEY = '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'
AWS_S3_HOST = 's3.ap-south-1.amazonaws.com'
AWS_S3_CALLING_FORMAT = 'boto.s3.connection.OrdinaryCallingFormat'
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_CUSTOM_DOMAIN = '%s' % AWS_STORAGE_BUCKET_NAME


conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY,
                    host=AWS_S3_HOST,
                    calling_format=OrdinaryCallingFormat())
bucket = conn.get_bucket(AWS_STORAGE_BUCKET_NAME)

print bucket
