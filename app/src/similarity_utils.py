import time
import sys

# globals
default_use_model = 'https://tfhub.dev/google/universal-sentence-encoder-large/3?tf-hub-format=compressed'
default_csv_file_path = './data/articles_small.csv'

default_batch_size = 10
default_stop_words = False
default_vector_size = 512
default_elasticindex_name = 'sentence_similarity'
default_elastic_server = 'http://elastic:Elastic123@localhost:9200/'
default_bootstrap_servers = ['localhost:9092']


# for new articles (articles1.csv)
g_columns = ['id', 'title', 'publication', 'content']
g_id_index = 0
g_content_index = 3
g_content_key = 'content'

def print_with_time(msg):
  print('{}: {}'.format(time.ctime(), msg))
  sys.stdout.flush()
