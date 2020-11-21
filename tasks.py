from __future__ import absolute_import
import time
import mysql.connector as mysql
import sys
sys.path.append('/home/daniele/Mimir-ApiServer')
from models import Notebook
from config import db
from celery import Celery

app = Celery('tasks', 
	broker= 'pyamqp://daniele:rabbitDD@localhost:5672/ddvhost', 
	backend= 'rpc://'
	)

db = mysql.connect(
    host= "localhost",
    user = "root",
    passwd="0satellite0",
    database= "mimir"
    )

@app.task
def longtime_add(id):
    if id is not None:
        cur = db.cursor()
        cur.execute("UPDATE mimir.notebook SET status ='created' WHERE id = '%d'" % id)
        db.commit()
        return 1
    else:
        return 0