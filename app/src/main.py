from flask import Flask, request
from flask_cors import CORS

import json
from json import JSONEncoder

from app.src.add_to_elasticindex import start_indexing, add_new_document_to_es
from app.src.document_producer import push_document_to_queue
from app.src.get_recommendations import get_recommended_documents, close_session

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['DEBUG'] = True

@app.route('/', methods=['GET'])
def home():
  return '<h1>Sentense Analysis</h1><p>Simple sentense analysis.</p>'

@app.route('/api/start-indexing-all', methods=['POST'])
def start_sentence_indexing():
  """Begin to index all sentences
  :param params: {
    use_model: 'required: googles-tfhub-model-url',
    data_source: 'required: data-source-that-needs-to-be-trained',
    data_columns: 'optional: column names of the data source',
    vector_size: 'optional: size-of-the-vector' (default: 512),
    stop_words: optional: boolean (default: False),
    batch_size: optional: Numeric (default: 32),
    elastic_server: 'optional: location for the elastic' (default: localhost@9200)
    elasticindex_name: 'optional: name for elastic indexing' (default: articles_small),
    
  }
  :return: success - result object with success message, 
            failure - result object with error message
  """
  params = request.get_json()
  result = start_indexing(params)
  return json.dumps(result)

@app.route('/api/add-document', methods=['POST'])
def add_document():
  """Add new document to the queue
  :param params: {
    payload: 'required: contains id, content and entity',
      id: 'optional: unique id for this document',
      title: 'title of the news content',
      publication: 'news publication,
      content: 'required: news content'

    use_model: 'required: googles-tfhub-model-url',
    data_columns: 'optional: column names of the data source',
    vector_size: 'optional: size-of-the-vector' (default: 512),
    stop_words: optional: boolean (default: False),
    elastic_server: 'optional: location for the elastic' (default: localhost@9200)
    elasticindex_name: 'optional: name for elastic indexing' (default: articles_small),
    bootstrap_servers: 'optional: list of bootstrap servers
  }
  :return: success - result object with success message, 
            failure - result object with error message
  """
  params = request.get_json()
  result = push_document_to_queue(params, params.get('payload'))
  return json.dumps(result)

@app.route('/api/search', methods=['POST'])
def get_recommendations():
  """Get top 3 documents related to the search string
  :param params: {
    search_string: 'required: search string,
    use_model: 'optional: googles-tfhub-model-url',
    elastic_server: 'optional: location for the elastic' (default: localhost@9200),
    elasticindex_name: 'optional: name for elastic indexing' (default: articles_small)
  }
  :return: success - result object with success message, 
            failure - result object with error message
  """
  params = request.get_json()
  result = get_recommended_documents(params, params.get('payload'))
  return json.dumps(result)

@app.route('/api/add-document-sync', methods=['POST'])
def add_document_sync():
  """Add new document to ES synchronously
  :param params: {
    payload: 'required: contains id, content and entity',
      id: 'optional: unique id for this document',
      title: 'title of the news content',
      publication: 'news publication,
      content: 'required: news'
    use_model: 'required: googles-tfhub-model-url',
    data_columns: 'optional: column names of the data source',
    vector_size: 'optional: size-of-the-vector' (default: 512),
    stop_words: optional: boolean (default: False),
    elastic_server: 'optional: location for the elastic' (default: localhost@9200)
    elasticindex_name: 'optional: name for elastic indexing' (default: articles_small)
  }
  :return: success - result object with success message, 
            failure - result object with error message
  """
  params = request.get_json()
  result = add_new_document_to_es(params, params.get('payload'))
  return json.dumps(result)

@app.route('/api/shutdown', methods=['GET'])
def shutdown():
  """Test API to close the TF session
  :return: success - result object with success message, 
            failure - result object with error message
  """
  result = close_session()
  return json.dumps(result)

if __name__ == '__main__':
  try:
    app.run(host='0.0.0.0', port=1975, debug=True)
  finally:
    print ('Closing flask server')
