from flask import Flask, request
from flask_cors import CORS

import json
from json import JSONEncoder

from app.src.add_to_elasticindex import start_indexing, add_new_document_to_es
from app.src.document_producer import push_document_to_queue
from app.src.get_recommendations import get_recommended_documents

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

app.config['DEBUG'] = True

@app.route('/', methods=['GET'])
def home():
  return '<h1>Sentense Analysis</h1><p>Simple sentense analysis.</p>'

@app.route('/start-indexing-all', methods=['POST'])
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

  if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1975, debug=True)

@app.route('/add-document', methods=['POST'])
def add_document():
  """Add new document to the queue
  :param params: {
    payload: 'required: contains id, content and entity',
      id: 'optional: unique id for this document',
      content: 'required: document content',
      entity: 'required: document entity'

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

@app.route('/get-recommendations', methods=['POST'])
def get_recommendations():
  """Add new document to the queue
  :param params: {
    content: 'required: column names of the data source',
    use_model: 'required: googles-tfhub-model-url',
    elastic_server: 'optional: location for the elastic' (default: localhost@9200),
    elasticindex_name: 'optional: name for elastic indexing' (default: articles_small)
  }
  :return: success - result object with success message, 
            failure - result object with error message
  """
  params = request.get_json()
  result = get_recommended_documents(params, params.get('content'))
  return json.dumps(result)

@app.route('/add-document-sync', methods=['POST'])
def add_document_sync():
  """Add new document to ES
  :param params: {
    payload: 'required: contains id, content and entity',
      id: 'optional: unique id for this document',
      content: 'required: document content',
      entity: 'required: document entity'
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


  if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1975, debug=True)
