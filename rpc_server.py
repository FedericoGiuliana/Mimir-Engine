import pika
from tasks import createNotebook, deleteNotebook
import json

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

channel = connection.channel()
channel.queue_declare(queue='rpc_queue')

def on_request(ch, method, props, body):

	message = json.loads(body)

	if(message.get("action") == 'Create'):
		response = createNotebook(message) 
	else:
		response = deleteNotebook(message)

	ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
	
	ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

print(" [x] Awaiting RPC requests. To exit press CTRL+C ")
channel.start_consuming()