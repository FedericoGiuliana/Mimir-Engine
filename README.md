# Start the engine for use the Notebook-jupyter 

## Getting Started

### Requirements

This project needs:

```
pipenv installed
Docker installed
Python 3.7 installed
Minikube installed
Celery installed
Rabbitmq installed
```

## Setup and launch engine
### Configure the environment

```
pipenv install --dev
pipenv shell
```
Start minikube with the command:
```
minikube start
```
 
Starting with setting the following environment variables:
```
CELERY_BROKER
CELERY_BACKEND
```
Setting the local dns as described in the README in the Jupyter folder

### Connecting Engine with API-server and create/delete a notebook-jupyter
Open 4 terminal:

On first terminal start the API-SERVER following this repository: https://github.com/dandamico/Mimir-ApiServer.git

On the second launch rabbitmq with command:
```
sudo rabbitmq-server
```

On the third  enter in Mimir-Engine folder and launch the celery worker with command:
```
celery -A celery worker --loglevel=info
```

On the latest terminal, to listen to the rabbitmq server, launch the command:
```
python rpc_server.py
```

Now browse to [http://localhost:5001/api/ui](http://localhost:5001/api/ui) to access SwaggerUI and execute a POST/notebook. Now 



