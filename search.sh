#!/bin/bash
get_payload()
{
  cat <<EOF
{
  "payload": {
    "content": "Health Care"
  }
}
EOF
}

curl -i \
-H "Accept: application/json" \
-H "Content-Type:application/json" \
-X POST --data "$(get_payload)" "http://127.0.0.1:1975/api/search"
