import tempfile

import boto3
from django.conf import settings

s3 = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_S3_REGION_NAME
)


def upload_file_to_s3(file, key):
    s3.upload_fileobj(file,
                      settings.AWS_STORAGE_BUCKET_NAME,
                      key)

def download_file_from_s3(key):
    tmp = tempfile.NamedTemporaryFile(delete=False)
    s3.download_fileobj(settings.AWS_STORAGE_BUCKET_NAME, key, tmp)
    tmp.seek(0)

    return tmp
