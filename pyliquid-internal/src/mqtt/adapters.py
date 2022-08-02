import pika  # type: ignore

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
