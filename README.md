# Download the zip files from minIO in Python using Boto3 and upload the unzipped file

## Getting Started

### Requirements

This project needs:

```
pipenv installed
Docker installed
Python 3.7 installed
Minikube installed
```

### Setup and uploading
Configure the environment :
```
pipenv shell
```
Start minikube with the command:
```
minikube start
```
 
Create the container and start MinIO:
```
docker run -t -d -p 9000:9000 --name miniozf \
-e "MINIO_ACCESS_KEY=admin" \
-e "MINIO_SECRET_KEY=keystone" \
-v /home/usr/mdata:/data \
minio/minio server /data
```

There must be a bucket inside with a zip folder inside. Inside the folder two files.

## There are 3 different ways to start the application:
### 1. Start the application locally:
Set the environment variables

Enter the Estrazione/App folder and start the python program estrazione.py:
```
python estrazione.py
```

### 2. Start the application with docker:
We need to reach MinIO, it is running on the host from within the container. On Linux you do this:
```
ip a
```

Create the docker image:
```
docker build -f Dockerfile -t estrazione .
```

I start the container by passing it the environment variables:
```
docker run -e ENDPOINT=http://172.17.0.1:9000 -e MINIO_ACCESS_KEY=admin -e MINIO_SECRET_KEY=keystone estrazione 
```

### 3. Start the application on kubernetes:
Now open the jobs.yaml file and set your credentials

Use kubectl to send the YAML file to Kubernetes by running the following command:
```
kubectl create -f job.yaml
```
You can see the jods are running if you execute the following command:
```
kubectl get jobs
```

You can see the pods are running if you execute the following command:
```
kubectl get po
```

Delete job with the command:
```
kubectl delete [JOBS' NAME]
```
### 4. Start the application on kubernetes by python:
Enter the Estrazione/App folder and start the python program creazionejob.py:
```
python creazionejob.py
```

