# sentence-similarity-with-elasticindexing
Short news articles lookup using Google's USE (Universal Sentence Encoder) and Elastic Indexing

## Installation

### Clone the repo
```
git clone https://github.com/Efficacy-Consulting/sentence-similarity-with-elasticindexing.git
cd sentence-similarity-with-elasticindexing/
```

## Run the application
1. Start `elasticsearch` instance (refer Usage section below) - `~/softwares_and_tools/elasticsearch-7.12.0/bin/elasticsearch`
2. Start `zookeeper` (refer Usage section below) - `~/softwares_and_tools/kafka_2.13-2.7.0/bin/zookeeper-server-start.sh ~/softwares_and_tools/kafka_2.13-2.7.0/config/zookeeper.properties`
3. Start `Kafka` (refer Usage section below) - `~/softwares_and_tools/kafka_2.13-2.7.0/bin/kafka-server-start.sh ~/softwares_and_tools/kafka_2.13-2.7.0/config/server.properties`
4. To run the flask server

    `a. Menu --> Run --> Run Without Debugging`

    (or)

    `b. Menu --> Run --> Start Debugging`

5. Open another terminal and run

    * To store document embedding into Elasticsearch for the 1st time (need to perform this only one)

      `./start_indexing.sh`

    * For any subsequent document addition, use kafka stream

      * Make sure you are in the right conda environment, otherwise run `conda activate tensorflow_env`

      * Start a kafka consumer
      
        `export PYTHONPATH="${PYTHONPATH}:app/src/"`

        `python app/src/document_consumer.py`

      * Run `./add_new_document.sh` to add new document using kafka producer

6. Finally, get `Elasticvue` chrome plugin and go to _`INDICES`_ and choose `articles_small` from there, use `./app/src/queries.json` to use as custom query

<hr>

## Usage
1. From VS Code, select **Python Interpreter** (`command+shift+p`) and choose `Python 3.7.6 64-bit ('tensorflow_env':conda)` (this is specific on my machine)

    - also activate tensorflow_env in the terminal also: `conda activate tensorflow_env`

2. Start `elasticsearch` instance
```
~/softwares_and_tools/elasticsearch-7.12.0/bin/elasticsearch
```

  - start zookeeper
    ```
    ~/softwares_and_tools/kafka_2.13-2.7.0/bin/zookeeper-server-start.sh ~/softwares_and_tools/kafka_2.13-2.7.0/config/zookeeper.properties
    ```

  - start kafka
    ```
    ~/softwares_and_tools/kafka_2.13-2.7.0/bin/kafka-server-start.sh ~/softwares_and_tools/kafka_2.13-2.7.0/config/server.properties
    ```
      - to stop kafka
        ```
        ~/softwares_and_tools/kafka_2.13-2.7.0/bin/kafka-server-stop.sh
        ```
      - clean up
        ```
        rm -rf /tmp/kafka-logs /tmp/zookeeper
        ```

<hr>

## Settings
### Elasticsearch
Added to `~softwares_and_tools/elasticsearch-7.12.0/config/elasticsearch.yml` inorder to avoid the following ES exception

_Elasticsearch exception [type=cluster_block_exception, reason=index [myindex] blocked by: [TOO_MANY_REQUESTS/12/index read-only / allow delete (api)];]_
```
cluster.routing.allocation.disk.threshold_enabled: true 
cluster.routing.allocation.disk.watermark.flood_stage: 200mb
cluster.routing.allocation.disk.watermark.low: 500mb 
cluster.routing.allocation.disk.watermark.high: 300mb
```

To set password
```
1. xpack.security.enabled: true
2. Start elasticsearch - ~/softwares_and_tools/elasticsearch-7.12.0/bin/elasticsearch
3. Run this command in another terminal ~/softwares_and_tools/elasticsearch-7.12.0/bin/elasticsearch-setup-passwords interactive
4. Stop and start elastic search
```

### Kafka
Checkout [Kafka Quickstart Guide](https://kafka.apache.org/quickstart)
1. Open the port
```
listeners=PLAINTEXT://:9092
```

2. Enable option to delete topic
```
delete.topic.enable=true
```