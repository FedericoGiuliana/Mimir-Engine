# Download zip files from minIO in Python using Boto3

## Getting Started

### Requirements

This project needs:
pipenv
```
pip install pipenv
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

Use pull command to download the lastest MinIO docker image:
```
docker pull minio/minio
```

Use pull command to download the 'estrazione' docker image:
```
docker pull ziofededocker/estrazione
```

Create the container and start MinIO:
```
docker run -t -d -p 9000:9000 --name miniozf \
-e "MINIO_ACCESS_KEY=admin" \
-e "MINIO_SECRET_KEY=keystone" \
-v /home/usr/mdata:/data \
minio/minio server /data
```

There must be a bucket named "bucketzf" inside with a zip folder inside named "Compressa.zip. Inside the folder two files, 'testo.txt' and 'model.py' and a second bucket named "bucketzf2".


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
kubectl delete jobs [JOBS' NAME]
```
