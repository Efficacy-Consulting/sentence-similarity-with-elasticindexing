#!/bin/bash
id=$1
title=$2
publication=$3
sentence=$4

generate_new_document()
{
  cat <<EOF
{
  payload: {
    id: $id,
    title: $title,
    publication: $publication,
    content: $sentence
  }
}
EOF
}

curl -i \
-H "Accept: application/json" \
-H "Content-Type:application/json" \
-X POST --data "$(generate_new_document)" "http://127.0.0.1:1975/add-document"
