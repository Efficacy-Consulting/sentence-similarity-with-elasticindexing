import time
import sys

# globals
default_use_model = 'https://tfhub.dev/google/universal-sentence-encoder-large/3?tf-hub-format=compressed'
default_csv_file_path = './data/articles_small.csv'

default_batch_size = 10
default_stop_words = False
default_vector_size = 512
default_elasticindex_name = 'articles_small'
default_elastic_server = 'http://elastic:Elastic123@localhost:9200/'
default_bootstrap_servers = ['localhost:9092']

g_columns = ['id', 'title', 'publication', 'content']
g_id_index = 0
g_content_index = 1
g_content_key = 'content'

g_mapping = {
  'mappings': {
    'properties': {
      'id': {
        'type': 'text'
      },
      'title': {
        'type': 'text'
      },
      'publication': {
        'type': 'text'
      },
      'content': {
        'type': 'text'
      },
      'embedding': {
        'type': 'dense_vector',
        'dims': default_vector_size
      }
    }
  }
}

def print_with_time(msg):
  print('{}: {}'.format(time.ctime(), msg))
  sys.stdout.flush()
