curl -X POST -H "Content-Type:application/json;" \
--data '{"data_source":"./data/short_wiki.csv"}' \
http://127.0.0.1:1975/start-indexing-all
