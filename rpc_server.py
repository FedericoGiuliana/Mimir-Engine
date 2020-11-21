import pika
from tasks import longtime_add
'''
import mysql.connector as mysql
import sys
sys.path.append('/home/daniele/Mimir-ApiServer')
from models import Notebook
from config import db



db = mysql.connect(
    host= "localhost",
    user = "root",
    passwd="0satellite0",
    database= "mimir"
    )

def fib(id):

    if id is not None:
        cur = db.cursor()
        cur.execute("UPDATE mimir.notebook SET status ='created' WHERE id = '%d'" % id)
        db.commit()
        return 1
    else:
        return 0
'''
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

channel = connection.channel()
channel.queue_declare(queue='rpc_queue')

def on_request(ch, method, props, body):
    n = int(body)

    print(" [.] fib(%s)" % n)
    response = longtime_add(n)  #change fib with longtime_add

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()