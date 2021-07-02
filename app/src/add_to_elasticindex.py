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
        ignore=400  # ignore 400 already exists code
    )


def get_es_instance():
    # connect to the elastic cluster
    # es = Elasticsearch([{'host': 'localhost', 'port': 9200}], http_auth=('user', 'pass'))
    elastic_client = Elasticsearch([default_elastic_server])

    return elastic_client


def create_index(params, data_frame, content_index):
    use_model = default_use_model
    stop_words = default_stop_words
    batch_size = default_batch_size
    elasticindex_name = default_elasticindex_name

    try:
        if params.get('use_model'):
            use_model = params.get('use_model')
        if params.get('stop_words'):
            stop_words = params.get('stop_words')
        if params.get('batch_size'):
            batch_size = params.get('batch_size')
        if params.get('elasticindex_name'):
            elasticindex_name = params.get('elasticindex_name')

        es = get_es_instance()
        if not es.indices.exists(elasticindex_name):
            add_index_mapping(es, elasticindex_name)

        start_time = time.time()
        print('USE model name', use_model)
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
        add_to_es_index(es, elasticindex_name, embedding,
                        batch_size, sentences,
                        content_array, stop_words, content_index)
        end_time = time.time()
        print_with_time('Add to ES Index Time: {}'.format(
            end_time - start_time))

    except Exception as e:
        raise


def add_to_es_index(es, elasticindex_name, embedding_fun, batch_size, sentences, content_array, stop_words, content_index):
    batch_contents = []
    batch_indexes = []
    batch_ids = []
    batch_entities = []
    last_indexed = 0
    num_batches = 0
    content = ''

    with tf.compat.v1.Session() as sess:
        sess.run([tf.compat.v1.global_variables_initializer(),
                  tf.compat.v1.tables_initializer()])
        for sindex, row in enumerate(content_array):
            content = row[content_index]
            if stop_words:
                content = remove_stopwords(row[content_index])

            batch_contents.append(content)
            batch_indexes.append(sindex)
            # id
            batch_ids.append(row[0])

            # entities
            batch_entities.append(row[2])

            if len(batch_contents) == batch_size:
                context_embed = sess.run(embedding_fun, feed_dict={
                    sentences: batch_contents})

                for index in batch_indexes:
                    document_dict = {
                        'ID':  batch_ids[index - last_indexed],
                        'CONTENT': batch_contents[index - last_indexed],
                        'ENTITY':  batch_entities[index - last_indexed],
                        'EMBEDDING': context_embed[index - last_indexed]
                    }
                    res = es.index(index=elasticindex_name, body=document_dict)

                batch_contents = []
                batch_indexes = []

                last_indexed += batch_size
                if num_batches % 10000 == 0:
                    print_with_time('sindex: {}'.format(sindex))

                num_batches += 1

        if batch_contents:
            context_embed = sess.run(embedding_fun, feed_dict={
                sentences: batch_contents})
            for index in batch_indexes:
                document_dict = {
                    'ID':  batch_ids[index - last_indexed],
                    'CONTENT': batch_contents[index - last_indexed],
                    'ENTITY':  batch_entities[index - last_indexed],
                    'EMBEDDING': context_embed[index - last_indexed]
                }
                res = es.index(index=elasticindex_name, body=document_dict)


def add_new_document_to_es(params, payload):
    result = {}
    use_model = default_use_model
    stop_words = default_stop_words
    elasticindex_name = default_elasticindex_name
    try:
        es = get_es_instance()

        if params.get('use_model'):
            use_model = params.get('use_model')
        if params.get('stop_words'):
            stop_words = params.get('stop_words')
        if params.get('elasticindex_name'):
            elasticindex_name = params.get('elasticindex_name')

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
        batch_contents = []
        batch_contents.append(payload['content'])
        with tf.compat.v1.Session() as sess:
            sess.run([tf.compat.v1.global_variables_initializer(),
                      tf.compat.v1.tables_initializer()])
            context_embed = sess.run(embedding, feed_dict={
                sentences: batch_contents})

        id = payload['id']
        if not id:
            id = int(round(time.time() * 1000))
        sentence_dict = {
            'id':  id,
            'content':  payload['content'],
            'entity':  payload['entity'],
            'embedding': context_embed[0]
        }
        res = es.index(index=elasticindex_name, body=sentence_dict)
        end_time = time.time()
        print_with_time('Adding new document ES: {}'.format(
            end_time - start_time))

    except Exception as e:
        print('Exception in push_document_to_queue: {0}'.format(e))
        result = {
            'error': 'Exception in push_document_to_queue: {0}'.format(e)
        }

    return result


def start_indexing(params):
    result = {}
    data_source = default_csv_file_path
    data_columns = g_columns

    print('Start Indexing', params)

    try:
        if params:
            if params.get('data_source'):
                data_source = params.get('data_source')
            if params.get('data_columns'):
                data_columns = params.get('data_columns')

        if(len(data_source) == 0):
            result = {
                'error': 'Invalid Input'
            }
        else:
            data_frame = pd.read_csv(data_source, usecols=g_columns)
            print_with_time('Data frame read from: ' + data_source)
            create_index(params, data_frame, g_content_index)

    except Exception as e:
        print('Exception in start_indexing: {0}'.format(e))
        result = {
            'error': 'Exception in start_indexing: {0}'.format(e)
        }

    return result
