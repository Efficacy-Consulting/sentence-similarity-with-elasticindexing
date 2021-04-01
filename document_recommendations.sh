#!/bin/bash
content=$1

get_payload()
{
  cat <<EOF
{
  "content": "$content"
}
EOF
}

curl -i \
-H "Accept: application/json" \
-H "Content-Type:application/json" \
-X POST --data "$(get_payload)" "http://127.0.0.1:1975/get-recommendations"
