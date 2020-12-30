#!/usr/bin/env/python
import os
import zipfile
import boto3
from botocore.client import Config




ENDPOINT=os.environ.get("ENDPOINT")
MINIO_ACCESS_KEY=os.environ.get("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY=os.environ.get("MINIO_SECRET_KEY")
BUCKET=os.environ.get("BUCKET")
FILEPATH=os.environ.get("FILEPATH")
FILENAME=os.environ.get("FILENAME")
ID_TRAINING=os.environ.get("ID_TRAINING")


s3 = boto3.resource('s3',
                    endpoint_url=ENDPOINT,
                    aws_access_key_id=MINIO_ACCESS_KEY,
		            aws_secret_access_key=MINIO_SECRET_KEY,
                    config=Config(signature_version='s3v4'),
                    region_name='us-east-1')


s3.Bucket(BUCKET).download_file(FILENAME, FILENAME)

path, ext = os.path.splitext(FILENAME)

if (ext==".zip"):
	archivio = zipfile.ZipFile(FILENAME) 


	# estrazione di tutti i file
	archivio.extractall() 

	#chiusura
	archivio.close()

	for file in os.listdir(path):
		
		s3.Bucket(BUCKET).upload_file(path+"/"+file, ID_TRAINING+"-"+file )
else:

	s3.Bucket(BUCKET).upload_file(FILENAME, ID_TRAINING+"-"+FILENAME)

print ("Scaricato file e ricaricato con id-training nel nome")

