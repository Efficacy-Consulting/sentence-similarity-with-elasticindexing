# Import KafkaProducer from Kafka library
from kafka import KafkaProducer

# Import JSON module to serialize data
import json
from app.src.similarity_utils import *

def push_document_to_queue(params, payload):
  result = {}
  bootstrap_servers = default_bootstrap_servers
  elasticindex_name = default_elasticindex_name

  if payload is None or bool(payload):
    result = {
      'error': 'Invalid argument - payload'
    }
    return result

  try:
    if params.get('bootstrap_servers'):
      bootstrap_servers = params.get('bootstrap_servers')
    if params.get('elasticindex_name'):
      elasticindex_name = params.get('elasticindex_name')

    start_time = time.time()
    # Initialize producer variable and set parameter for JSON encode
    producer = KafkaProducer(bootstrap_servers=default_bootstrap_servers,
                            value_serializer=lambda x: 
                            json.dumps(x).encode('utf-8'))

    end_time = time.time()
    print_with_time('Create Kafka Producer: {}'.format(end_time-start_time))


    start_time = time.time()
    producer.send(default_elasticindex_name, payload)
    end_time = time.time()
    print_with_time('Push to queue the module: {}'.format(end_time-start_time))

  except Exception as e:
    print('Exception in push_document_to_queue: {0}'.format(e))
    result = {
      'error': 'Exception in push_document_to_queue: {0}'.format(e)
    }
  finally:
    producer.close()
  
  return result
