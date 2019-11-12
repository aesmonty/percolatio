import os
from conduit.settings.common import *

import boto3
ssm = boto3.client('ssm', region_name='eu-west-2')


def _get_ssm_key(name):
    key = ssm.get_parameter(Name=name, WithDecryption=True)
    return key['Parameter']['Value']


DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

SECRET_KEY = _get_ssm_key('/Dev/WebServer/Secret')

DEBUG = False

ALLOWED_HOSTS = ['0.0.0.0', 'conduit.eu-west-2.elasticbeanstalk.com']

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

CORS_ORIGIN_WHITELIST = (
    'conduit.eu-west-2.elasticbeanstalk.com',
)

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_STORAGE_BUCKET_NAME = "percolatio.images"
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = False
