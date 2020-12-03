import mysql.connector as mysql
from celery import Celery
from Jupyter.CreaJupyter import crea
from Jupyter.CancellaJupyter import cancella
import os

MYSQL_PSSW = os.environ.get("MYSQL_PASSWORD")
MYSQL_HOST = os.environ.get("MYSQL_HOST")
MYSQL_USER = os.environ.get("MYSQL_USER")
CELERY_BROKER= os.environ.get("CELERY_BROKER")
CELERY_BACKEND= os.environ.get("CELERY_BACKEND")
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
        crea()
        
        cur = db.cursor()
        cur.execute("UPDATE mimir.notebook SET status ='created' WHERE id = '%d'" % int(message.get('id')))
        db.commit()
        return print("[.] Successfully look db")
    else:
        return print("[.] Sorry, see around")

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