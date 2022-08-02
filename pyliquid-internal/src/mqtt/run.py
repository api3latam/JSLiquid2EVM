import pika  # type: ignore

connection = pika.SelectConnection()

if __name__ == "__main__":
    try:
        connection.ioloop.start()
    except KeyboardInterrupt:
        connection.close()
