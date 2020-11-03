#!/usr/bin/env/python
import os
import zipfile
import boto3
from botocore.client import Config



ENDPOINT=os.environ.get("ENDPOINT")
MINIO_ACCESS_KEY=os.environ.get("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY=os.environ.get("MINIO_SECRET_KEY")

s3 = boto3.resource('s3',
                    endpoint_url=ENDPOINT,
                    aws_access_key_id=MINIO_ACCESS_KEY,
		     aws_secret_access_key=MINIO_SECRET_KEY,
                    config=Config(signature_version='s3v4'),
                    region_name='us-east-1')

# download the object 'compressa.zip' from the bucket 'bucketzf' and save it to local FS as Compressa.zip
s3.Bucket('bucketzf').download_file('Compressa.zip', 'Compressa.zip')

# apertura dell'archivio per estrazione
archivio = zipfile.ZipFile('Compressa.zip') 


# estrazione di tutti i file
archivio.extractall() 

#chiusura
archivio.close()

# upload a file from local file system '/testo.text' to bucket 'bucketzf2' with 'testo.txt' as the object name.
s3.Bucket('bucketzf2').upload_file('Compressa/testo.txt', 'testo.txt' )
# upload a file from local file system '/model.py' to bucket 'bucketzf2' with 'model.py' as the object name.
s3.Bucket('bucketzf2').upload_file('Compressa/model.py', 'model.py' )


print ("Scaricato file zip e ricaricato senza la compressione")

