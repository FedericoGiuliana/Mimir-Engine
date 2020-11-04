#!/usr/bin/env/python
import os
import zipfile
import boto3
from botocore.client import Config




ENDPOINT=os.environ.get("ENDPOINT")
MINIO_ACCESS_KEY=os.environ.get("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY=os.environ.get("MINIO_SECRET_KEY")

OBJECT_NAME=os.environ.get("OBJECT_NAME")
MODEL_FILE=os.environ.get("MODEL_FILE")
BUCKET=os.environ.get("BUCKET")

NAME_FILE=os.environ.get("NAME_FILE")
NAME_FILE1=os.environ.get("NAME_FILE1")
MODEL_DIR=os.environ.get("MODEL_DIR")

MODEL_PATH=os.path.join(MODEL_DIR, NAME_FILE)
MODEL_PATH1=os.path.join(MODEL_DIR, NAME_FILE1)


s3 = boto3.resource('s3',
                    endpoint_url=ENDPOINT,
                    aws_access_key_id=MINIO_ACCESS_KEY,
		            aws_secret_access_key=MINIO_SECRET_KEY,
                    config=Config(signature_version='s3v4'),
                    region_name='us-east-1')

# download the object 'compressa.zip' from the bucket 'bucketzf' and save it to local FS as Compressa.zip
s3.Bucket(BUCKET).download_file(OBJECT_NAME, MODEL_FILE)
# apertura dell'archivio per estrazione
archivio = zipfile.ZipFile(OBJECT_NAME) 


# estrazione di tutti i file
archivio.extractall() 

#chiusura
archivio.close()


# upload a file from local file system '/testo.text' to bucket 'bucketzf' with 'testo.txt' as the object name.
s3.Bucket(BUCKET).upload_file(MODEL_PATH, NAME_FILE )
# upload a file from local file system '/model.py' to bucket 'bucketzf' with 'model.py' as the object name.
s3.Bucket(BUCKET).upload_file(MODEL_PATH1, NAME_FILE1 )

print ("Scaricato file zip e ricaricato senza la compressione")

