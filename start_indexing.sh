curl -X POST -H "Content-Type:application/json;" \
--data '{"data_source":"./data/articles_small.csv"}' \
http://127.0.0.1:1975/api/start-indexing-all
