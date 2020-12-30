import mysql.connector as mysql
from celery import Celery
from Jupyter.CreaJupyter import crea
from Jupyter.CancellaJupyter import cancella
import os
from Estrazione.App.uploadfile import creaTraining
from Estrazione.App.creazionejob import creajob
import time

MYSQL_PSSW = os.environ.get("MYSQL_PASSWORD")
MYSQL_HOST = os.environ.get("MYSQL_HOST")
MYSQL_USER = os.environ.get("MYSQL_USER")
CELERY_BROKER= os.environ.get("CELERY_BROKER")
CELERY_BACKEND= os.environ.get("CELERY_BACKEND")
DOMAIN_NAME= os.environ.get("DOMAIN_NAME")

app = Celery('tasks', 
	broker= CELERY_BROKER, 
	backend= CELERY_BACKEND,
	)

db = mysql.connect(
    host= MYSQL_HOST,
    user = MYSQL_USER,
    passwd= MYSQL_PSSW,
    database= "mimir"
    )

@app.task
def createNotebook(message): 
    if message is not None:

        print(f"""
            ID: {message.get('id')}
            ACTION: {message.get('action')}
            """)

        crea(message.get("name")+"-"+str(message.get("id")))
        
        cur = db.cursor()
        cur.execute("UPDATE mimir.notebook SET status ='created' WHERE id = '%d'" % int(message.get('id')))
        db.commit()

        url=message.get("name")+"-"+str(message.get("id"))+DOMAIN_NAME

        cur = db.cursor()
        cur.execute("UPDATE mimir.notebook SET notebook_url ='%s' WHERE id = '%d'" % (url, int(message.get('id'))))
        db.commit()

        print("[.] Successfully look db")
        return print("[x] Awaiting RPC requests. To exit press CTRL+C ")
    else:
        print("[.] Sorry, see around")
        return print("[x] Awaiting RPC requests. To exit press CTRL+C ")

@app.task
def deleteNotebook(message): 
    if message is not None:

        print(f"""
            ID: {message.get('id')}
            ACTION: {message.get('action')}
            """)
        cancella()
        
        return print("[.] Successfully look db")
    else:
        return print("[.] Sorry, see around")

@app.task
def createTraining(message):
    if message is not None:
        print(f"""
            ID: {message.get('id')}
            ACTION: {message.get('action')}
            """)
        
        creaTraining(message.get("file_name"), message.get("file_path"))
        time.sleep(10)
        creajob(message.get("file_name"), message.get("file_path") , message.get("id"))
        
        cur = db.cursor()
        cur.execute("UPDATE mimir.training SET status ='created' WHERE id = '%d'" % int(message.get('id')))
        db.commit()
        print("[.] Successfully look db")
        return print("[x] Awaiting RPC requests. To exit press CTRL+C ")
    else:
        print("[.] Sorry, see around")
        return print("[x] Awaiting RPC requests. To exit press CTRL+C ")