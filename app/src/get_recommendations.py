import os
import json

import time
import sys

import tensorflow as tf
import tensorflow_hub as hub

from gensim.parsing.preprocessing import remove_stopwords

import pandas as pd
import numpy as np

from elasticsearch import Elasticsearch
from app.src.similarity_utils import *

def add_index_mapping(es, elasticindex_name):
  # make an API call to the Elasticsearch cluster
  # and have it return a response:
  response = es.indices.create(
      index=elasticindex_name,
      body=g_mapping,
      ignore=400 # ignore 400 already exists code
  )

def get_es_instance():
  # connect to the elastic cluster
  elastic_client = Elasticsearch([default_elastic_server])

  return elastic_client

def get_recommended_documents(params, content):
  result = {}
  use_model = default_use_model
  stop_words = default_stop_words
  batch_size = default_batch_size
  elasticindex_name = default_elasticindex_name

  try:
    if params.get('use_model'):
      use_model = params.get('use_model')
    if params.get('elasticindex_name'):
      elasticindex_name = params.get('elasticindex_name')

    if content is None:
      result = {
        'error': 'Invalid argument - content'
      }
      return result

    es = get_es_instance()
    if not es.indices.exists(elasticindex_name):
        return "No records found"

    start_time = time.time()
    embed_func = hub.Module(use_model)
    end_time = time.time()
    print_with_time('Load the module: {}'.format(end_time-start_time))

    start_time = time.time()
    sentences = tf.compat.v1.placeholder(dtype=tf.string, shape=[None])
    embedding = embed_func(sentences)
    end_time = time.time()
    print_with_time('Init sentences embedding: {}'.format(end_time-start_time))

    start_time = time.time()
    batch_sentences = []
    batch_sentences.append(content)
    with tf.compat.v1.Session() as sess:
      sess.run([tf.compat.v1.global_variables_initializer(),
                tf.compat.v1.tables_initializer()])
      vector = sess.run(embedding, feed_dict={
          sentences: batch_sentences})

    query_vec = np.asarray(vector).tolist()

    start_time = time.time()
    script_query = {
      "query": {
        "script_score": {
          "query": {
            "match_all": {}
          },
          "script": {
            "source": "(cosineSimilarity(params.query_vector, 'EMBEDDING') + 1.0)",
            "params": {
              "query_vector": query_vec[0]
            }
          }
        }
      },
      "_source": [
        "ID",
        "ENTITY",
        "CONTENT"
      ]
    }

    result = es.search(index=elasticindex_name, body=script_query)
    total_match = len(result["hits"]["hits"])
    print("Total Matches: ", str(total_match))
    # print(result)
    thresh = 1.2
    top_n = 10
    data = []
    if total_match > 0:
      q_ids = []
      for hit in result["hits"]["hits"]:
        if hit['_score'] > thresh and len(data) <= top_n:
          # print("--\nscore: {} \n question: {} \n answer: {}\n--".format(hit["_score"], hit["_source"]['question'], hit["_source"]['answer']))
          q_ids.append(hit['_source']['ID'])
          data.append(
            { 
              'ID': hit["_source"]['ID'],
              'CONTENT': hit["_source"]['CONTENT'],
              'ENTITY': hit["_source"]['ENTITY'],
            })

    result = {
      "data": data
    }
    end_time = time.time()
    print_with_time('Search from ES Time: {}'.format(end_time - start_time))

  except Exception as e:
    print('Exception in get_recommended_documents: {0}'.format(e))
    result = {
      'error': 'Exception in get_recommended_documents: {0}'.format(e)
    }

  return result