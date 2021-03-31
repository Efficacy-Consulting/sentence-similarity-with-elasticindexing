# Import KafkaConsumer from Kafka library
from kafka import KafkaConsumer

import os
import json

import re
import sys

from app.src.add_to_elasticindex import add_new_document_to_es
from app.src.similarity_utils import print_with_time

# globals
topic_name = 'sentence-similarity'

def filter_sentence(sentence):
  # s1 = ''.join([i if ord(i) < 128 else ' ' for i in s])
  return re.sub(r'[^\x00-\x7F]+',' ', sentence)

def init_kafka():
  consumer = KafkaConsumer(topic_name,
                          bootstrap_servers=['localhost:9092'],
                          value_deserializer=lambda x: json.loads(x.decode('utf-8')))

  print_with_time('Ready for consuming new topics...')
  # Read data from kafka
  for message in consumer:
    print_with_time('\nReading from JSON data\n')
    print_with_time('id: ' +  message.value['id'])
    print_with_time('title: ' + message.value['title'])

    add_new_document_to_es({}, message.value)

if __name__ == '__main__':
    init_kafka()

    # Terminate the script
    # sys.exit()
