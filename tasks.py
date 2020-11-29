import mysql.connector as mysql
from celery import Celery

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
def createNotebook(id): 
    if id is not None:

        print(f"""
            ID: {id}
            ACTION: 'CREATION'
            """)
        
        cur = db.cursor()
        cur.execute("UPDATE mimir.notebook SET status ='created' WHERE id = '%d'" % int(id))
        db.commit()
        return print("[.] Successfully look db")
    else:
        return print("[.] Sorry, see around")
