from flask import Flask, request
from flask_cors import CORS

import json
from json import JSONEncoder

from app.src.add_to_elasticindex import start_indexing, add_new_document_to_es

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
    elasticindex_name: 'optional: name for elastic indexing' (default: sentence_similarity),
    
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
  """Begin to index all sentences
  :param params: {
    payload: 'required: contains id, title, publication and sentence',
      id: 'optional: unique id for this document',
      title: 'required: document title',
      publication: 'required: document publication',
      sentence: 'required: document content'
    use_model: 'required: googles-tfhub-model-url',
    data_columns: 'optional: column names of the data source',
    vector_size: 'optional: size-of-the-vector' (default: 512),
    stop_words: optional: boolean (default: False),
    batch_size: optional: Numeric (default: 32),
    elastic_server: 'optional: location for the elastic' (default: localhost@9200)
    elasticindex_name: 'optional: name for elastic indexing' (default: sentence_similarity),
    
  }
  :return: success - result object with success message, 
            failure - result object with error message
  """
  params = request.get_json()
  result = add_new_document_to_es(params, params.get('payload'))
  return json.dumps(result)

  if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1975, debug=True)
