#!/usr/bin/env/python
import os
import zipfile
import boto3
from botocore.client import Config




ENDPOINT=os.environ.get("ENDPOINT")
MINIO_ACCESS_KEY=os.environ.get("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY=os.environ.get("MINIO_SECRET_KEY")


BUCKET=os.environ.get("BUCKET")


def creaTraining(filename, filepath):
	s3 = boto3.resource('s3',
		                endpoint_url=ENDPOINT,
	    	            aws_access_key_id=MINIO_ACCESS_KEY,
		    	        aws_secret_access_key=MINIO_SECRET_KEY,
	            	    config=Config(signature_version='s3v4'),
	                	region_name='us-east-1')



	 
	Notexist=s3.Bucket(BUCKET) in s3.buckets.all()
	if Notexist==False:
		s3.create_bucket(Bucket=BUCKET)
		
	s3.Bucket(BUCKET).upload_file(filepath, filename)


	print ("Caricato file ")

