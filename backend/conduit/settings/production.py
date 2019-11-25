import os
from conduit.settings.common import *

import boto3
ssm = boto3.client('ssm', region_name='eu-west-2')

AWS_S3_REGION_NAME = 'eu-west-2'


def _get_ssm_key(name):
    key = ssm.get_parameter(Name=name, WithDecryption=True)
    return key['Parameter']['Value']


SECRET_KEY = _get_ssm_key('/Dev/WebServer/Secret')

DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0', 'http://percdev.eu-west-1.elasticbeanstalk.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['RDS_DB_NAME'],
        'USER': os.environ['RDS_USERNAME'],
        'PASSWORD': os.environ['RDS_PASSWORD'],
        'HOST': os.environ['RDS_HOSTNAME'],
        'PORT': os.environ['RDS_PORT'],
    }
}

CORS_ORIGIN_WHITELIST = ('http://percdev.eu-west-1.elasticbeanstalk.com',
                         'https://s3.eu-west-2.amazonaws.com/percolation.images/',
                         )

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'custom_storages.StaticStorage'

AWS_STORAGE_BUCKET_NAME = "percolation.images"
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = False
