#!/usr/bin/env/python
import os
import zipfile
import boto3
from botocore.client import Config




ENDPOINT=os.environ.get("ENDPOINT")
MINIO_ACCESS_KEY=os.environ.get("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY=os.environ.get("MINIO_SECRET_KEY")


BUCKET=os.environ.get("BUCKET")

NAME_FILE=os.environ.get("NAME_FILE")
MODEL_DIR=os.environ.get("MODEL_DIR")

MODEL_PATH=os.path.join(MODEL_DIR, NAME_FILE)


s3 = boto3.resource('s3',
                    endpoint_url=ENDPOINT,
                    aws_access_key_id=MINIO_ACCESS_KEY,
		            aws_secret_access_key=MINIO_SECRET_KEY,
                    config=Config(signature_version='s3v4'),
                    region_name='us-east-1')


# upload a file from local file system '/testo.text' to bucket 'bucketzf' with 'testo.txt' as the object name.
s3.Bucket(BUCKET).upload_file(MODEL_PATH, NAME_FILE )


print ("Caricato file zip ")

