import csv
import json
import logging
import os
import time
# import datetime as dt
# import kafka.errors
from dotenv import load_dotenv
from data_generator import generate_data
from kafka import KafkaProducer

load_dotenv()

data_path = os.getenv("stream_data_path")
list_topics = os.getenv("TOPICS").split(",")
bootstrap_servers = os.getenv("BOOTSTRAP_SERVERS", 'localhost:9091,localhost:9092,localhost:9093').split(',')
batch_size = int(os.getenv("batch_size"))
KAFKA_VERSION = tuple([int(v) for v in os.getenv("KAFKA_VERSION").split(",")])

# print(bootstrap_servers)
# print(list_topics)

# print('basename:    ', os.path.basename(__file__))
# print('dirname:     ', os.path.dirname(__file__))


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s:%(funcName)s:%(levelname)s:%(message)s"
)

# Messages will be serialized as JSON 
def serializer(message):
    return json.dumps(message).encode()


def setup_producer():
    """
    create a KafkaProducer instance with bootstrap servers.
    Parameters:
    Returns:
    - KafkaProducer instance.
    """    
    try:
        Kafka_producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=serializer
        )
        return Kafka_producer
    except Exception as e:
        if e == 'NoBrokersAvailable':
            print('waiting for brokers to become available')
        return 'not-ready'


def send_message(Kafka_producer, topic, messages):
    """
    Send masseges to a topic by producer.
    Args:
    - Kafka_producer (object): used to send messages.
    - topic (string): a name of topic.
    - message (list): a list of messages.
    Returns: None
    """
    try:
        for message in messages:
            # message['created_at']= dt.datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")
            # print("==================================")
            # print(message)
            # print("==================================")
            Kafka_producer.send(topic, value=message)
        # Wait for all messages in the Producer queue to be delivered
        Kafka_producer.flush()
        logging.info(f"Massesge Sent to topic '{topic}'.")
    except Exception as e:
        logging.error(
            f"Failed to send messages \
                            topic '{topic}'."
        )


def streaming(Kafka_producer):
    """
    Processing files and send the masseges.
    Args:
    - Kafka_producer (object):
    Returns: None
    """
    for topic in list_topics:
        try:
            list_of_rows = generate_data(data_path, topic) 
            if len(list_of_rows) >= batch_size:
                send_message(Kafka_producer, topic, list_of_rows)
                list_of_rows=[]
            if list_of_rows:
                # send the remianing messages in the list
                send_message(Kafka_producer, topic, list_of_rows)

        except FileNotFoundError:
            logging.error(f"file {data_path}/{topic} not found.")
        except Exception as e:
            logging.error(
                f"Failed to process the file and \
                                sending messages."
            )



if __name__ == "__main__":
    print('setting up producer, checking if brokers are available')
    Kafka_producer='not-ready'
    while Kafka_producer == 'not-ready':
        print('brokers not available yet')
        time.sleep(5)
        Kafka_producer = setup_producer()
    print('brokers are available and ready to produce messages')
    try:
        streaming(Kafka_producer)
    finally:
        Kafka_producer.close()


