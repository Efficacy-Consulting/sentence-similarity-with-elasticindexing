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
from utils import print_with_time

# globals
default_batch_size = 10

# for new articles (articles1.csv)
g_columns = ['id', 'title', 'publication', 'content']
g_id_index = 0
g_content_index = 3
g_content_key = 'content'

default_use_model = 'https://tfhub.dev/google/universal-sentence-encoder-large/3?tf-hub-format=compressed'
default_csv_file_path = './data/articles_small.csv'

stop_words = False

elasticindex_name = 'sentence_similarity'

params = {
    'data_file': default_csv_file_path,
    'use_model': default_use_model,
    'stop_words': stop_words,
    'default_batch_size': default_batch_size
}

def get_es_instance():
    mapping = {
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
                'sentence': {
                    'type': 'text'
                },
                'embedding': {
                    'type': 'dense_vector',
                    'dims': 512
                }
            }
        }
    }

    # connect to the elastic cluster
    # es = Elasticsearch([{'host': 'localhost', 'port': 9200}], http_auth=('user', 'pass'))
    elastic_client = Elasticsearch(['http://elastic:Elastic123@localhost:9200/'])

    # make an API call to the Elasticsearch cluster
    # and have it return a response:
    # response = elastic_client.indices.create(
    #     index=elasticindex_name,
    #     body=mapping,
    #     ignore=400 # ignore 400 already exists code
    # )

    return elastic_client


def create_index(params, data_frame, content_index):
    try:
        es = get_es_instance()
        data_file = params.get('data_file')
        use_model = params.get('use_model')
        stop_words = params.get('stop_words')
        default_batch_size = params.get('default_batch_size')

        start_time = time.time()
        embed_func = hub.Module(use_model)
        end_time = time.time()
        print_with_time('Load the module: {}'.format(end_time-start_time))

        start_time = time.time()
        sentences = tf.compat.v1.placeholder(dtype=tf.string, shape=[None])
        embedding = embed_func(sentences)
        end_time = time.time()
        print_with_time(
            'Init sentences embedding: {}'.format(end_time-start_time))

        start_time = time.time()
        content_array = data_frame.to_numpy()
        end_time = time.time()
        print_with_time('Read Data Time: {}'.format(end_time - start_time))

        start_time = time.time()
        add_to_es_index(es, embedding,
                          default_batch_size, sentences,
                          content_array, stop_words, content_index)
        end_time = time.time()
        print_with_time('Add to ES Index Time: {}'.format(end_time - start_time))

    except Exception as e:
        raise


def add_to_es_index(es, embedding_fun, batch_size, sentences, content_array, stop_words, content_index):
    batch_sentences = []
    batch_indexes = []
    batch_ids = []
    batch_titles = []
    batch_publications = []
    last_indexed = 0
    num_batches = 0
    content = ''

    with tf.compat.v1.Session() as sess:
        sess.run([tf.compat.v1.global_variables_initializer(),
                  tf.compat.v1.tables_initializer()])
        for sindex, sentence in enumerate(content_array):
            content = sentence[content_index]
            if stop_words:
                content = remove_stopwords(sentence[1])

            batch_sentences.append(content)
            batch_indexes.append(sindex)
            # id
            batch_ids.append(sentence[0])

            # title
            batch_titles.append(sentence[1])

            # publication
            batch_publications.append(sentence[2])

            if len(batch_sentences) == batch_size:
                context_embed = sess.run(embedding_fun, feed_dict={
                                         sentences: batch_sentences})

                for index in batch_indexes:
                    sentence_dict = {
                        'id':  batch_ids[index - last_indexed],
                        'title':  batch_titles[index - last_indexed],
                        'publication':  batch_publications[index - last_indexed],
                        'sentence': batch_sentences[index - last_indexed],
                        'embedding': context_embed[index - last_indexed]
                    }
                    res = es.index(index=elasticindex_name, body=sentence_dict)

                batch_sentences = []
                batch_indexes = []

                last_indexed += batch_size
                if num_batches % 10000 == 0:
                    print_with_time('sindex: {}'.format(sindex))

                num_batches += 1

        if batch_sentences:
            context_embed = sess.run(embedding_fun, feed_dict={
                sentences: batch_sentences})
            for index in batch_indexes:
                sentence_dict = {
                    'id':  batch_ids[index - last_indexed],
                    'title':  batch_titles[index - last_indexed],
                    'publication':  batch_publications[index - last_indexed],
                    'sentence': batch_sentences[index - last_indexed],
                    'embedding': context_embed[index - last_indexed]
                }
                res = es.index(index=elasticindex_name, body=sentence_dict)


def add_new_document_to_es(payload):
  try:
    es = get_es_instance()
    data_file = params.get('data_file')
    use_model = params.get('use_model')
    stop_words = params.get('stop_words')
    default_batch_size = params.get('default_batch_size')

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
    batch_sentences.append(payload['sentence'])
    with tf.compat.v1.Session() as sess:
      sess.run([tf.compat.v1.global_variables_initializer(),
                tf.compat.v1.tables_initializer()])
      context_embed = sess.run(embedding, feed_dict={
          sentences: batch_sentences})

    sentence_dict = {
        'id':  payload['id'],
        'title':  payload['title'],
        'publication':  payload['publication'],
        'sentence': payload['sentence'],
        'embedding': context_embed[0]
    }
    res = es.index(index=elasticindex_name, body=sentence_dict)
    end_time = time.time()
    print_with_time('Adding new document ES: {}'.format(end_time - start_time))

  except Exception as e:
    raise


if __name__ == '__main__':
    data_frame = pd.read_csv(default_csv_file_path, usecols=g_columns)
    print_with_time('Data frame read from: ' + default_csv_file_path)
    create_index(params, data_frame, g_content_index)
