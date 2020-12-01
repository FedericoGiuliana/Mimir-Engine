import mysql.connector as mysql
from celery import Celery
import time

app = Celery('tasks', 
	broker= 'pyamqp://daniele:rabbitDD@localhost:5672/ddvhost', 
	backend= 'pyamqp://daniele:rabbitDD@localhost:5672/ddvhost',
	)

db = mysql.connect(
    host= "localhost",
    user = "root",
    passwd="0satellite0",
    database= "mimir"
    )

@app.task
def createNotebook(message): 
    if message is not None:

        print(f"""
            ID: {message.get('id')}
            ACTION: {message.get('action')}
            """)

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
        
        time.sleep(5)
        return print("[.] Successfully look db")
    else:
        return print("[.] Sorry, see around")