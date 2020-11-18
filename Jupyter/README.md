# Create a Jupyter notebook

## Getting Started

### Requirements

This project needs:

```
pipenv installed
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
 
## There are 2 different ways to start the application:
### 1. Start the application on kubernetes by python:
Enter the Jupyter folder and start the python program CreaJupyter.py:
```
python CreaJupyter.py
```

Visit the service via NodePort:
```
minikube service jupyter-service --url
```

### 2. Start the application on kubernetes by yaml file:
Enter the Jupyter folder and create deployment and service:
```
kubectl create -f deployment.yaml
kubectl create -f service.yaml
```

Visit the service via NodePort:
```
minikube service jupyter-service --url
```
