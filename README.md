# sentence-similarity-with-elasticindexing
Short wikipedia articles lookup using Google's USE (Universal Sentence Encoder) and Elastic Indexing

## Installation

### Clone the repo
```
git clone https://github.com/Efficacy-Consulting/sentence-similarity-with-elasticindexing.git
cd sentence-similarity-with-elasticindexing/
```

### Install the required libs
```
pip install -r requirements.txt
```

## Settings
## Elasticsearch
Added to `~softwares_and_tools/elasticsearch-7.10.1/config/elasticsearch.yml` inorder to avoid the following ES exception

_Elasticsearch exception [type=cluster_block_exception, reason=index [myindex] blocked by: [TOO_MANY_REQUESTS/12/index read-only / allow delete (api)];]_
```
cluster.routing.allocation.disk.threshold_enabled: true 
cluster.routing.allocation.disk.watermark.flood_stage: 200mb
cluster.routing.allocation.disk.watermark.low: 500mb 
cluster.routing.allocation.disk.watermark.high: 300mb
```

## Kafka
Checkout [Kafka Quickstart Guide](https://kafka.apache.org/quickstart)
1. Open the port
```
listeners=PLAINTEXT://:9092
```

2. Enable option to delete topic
```
delete.topic.enable=true
```

## Usage
1. From VS Code, select **Python Interpreter** (`command+shift+p`) and choose `Python 3.7.6 64-bit ('tensorflow_env':conda)` (this is specific on my machine)

    - also activate tensorflow_env in the terminal also: `conda activate tensorflow_env`

2. Start `elasticsearch` instance
```
~/softwares_and_tools/elasticsearch-7.10.1/bin/elasticsearch
```

  - start zookeeper
    ```
    ~/softwares_and_tools/kafka_2.13-2.7.0/bin/zookeeper-server-start.sh config/zookeeper.properties
    ```

  - start kafka
    ```
    ~/softwares_and_tools/kafka_2.13-2.7.0/bin/kafka-server-start.sh config/server.properties
    ```
      - to stop kafka
        ```
        ~/softwares_and_tools/kafka_2.13-2.7.0/bin/kafka-server-stop.sh
        ```
      - clean up
        ```
        rm -rf /tmp/kafka-logs /tmp/zookeeper
        ```

3. Enter the following command in the terminal
```
python ./app/src/sentence-similarity-es.py
```
4. Get Elasticvue chrome plugin and go to _`INDICES`_ and choose `sentence-similarity` from there, use `./app/src/queries.json` to use as custom query
