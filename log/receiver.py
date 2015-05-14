from multiprocessing import Process

import pika
import json



def do_recv(rmChannel, method, properties, body):
	downItem = json.loads(body)

	

def receiver():
	

	rmCon = pika.BlockingConnection(pika.ConnectionParameters(host = 'mqs'))
	rmChannel = rmCon.channel()
	rmChannel.queue_declare(queue = 'ctod')

	rmChannel.basic_consume(do_recv, queue = 'ctod', no_ack = True)
	rmChannel.start_consuming()
