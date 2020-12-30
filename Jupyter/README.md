# Create and Delete a Jupyter notebook

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
enable ingress controller:
```
minikube addons enable ingress 
```

## There are 2 different ways to start the application:
### 1. Start the application on kubernetes by python:
Enter the Jupyter folder and start the python program CreaJupyter.py:
```
python CreaJupyter.py
```

Search  :
```
kubectl describe ingress jupyter-ingress

```

Open /ect/hosts file and set your local DNS with the name ".notebooks.kubernetes.local":
```
sudo vim /etc/hosts
```

Now you can find the jupyter notebook in your browser at host "http://pippo-1.notebooks.kubernetes.local"

### 2. Start the application on kubernetes by yaml file:
Enter the Jupyter folder and create deployment and service:
```
kubectl create -f deployment.yaml
kubectl create -f service.yaml
kubectl create -f ingress.yaml
```

Visit the service:
```
kubectl describe ingress jupyter-ingress
```

Open /ect/hosts file and set your local DNS with the name "pippo.notebooks.kubernetes.local":
```
sudo vim /etc/hosts
```

Now you can find the notebook jupyter in your browser at host "http://pippo-1.notebooks.kubernetes.local"


## Delete the jupyter notebook:
Enter the Jupyter folder and start the python program CancellaJupyter.py:
```
python CancellaJupyter.py
```
