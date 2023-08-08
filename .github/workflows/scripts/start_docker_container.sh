#!/bin/bash
set -e

# 引数がない場合は、環境変数を利用する
if [ $# -eq 0 ]; then
  SPOTIFY_CLIENT_ID=$SPOTIFY_CLIENT_ID
  SPOTIFY_CLIENT_SECRET=$SPOTIFY_CLIENT_SECRET
  NOTION_API_TOKEN=$NOTION_API_TOKEN
  ACCESS_TOKEN=$ACCESS_TOKEN
else
  SPOTIFY_CLIENT_ID=$1
  SPOTIFY_CLIENT_SECRET=$2
  NOTION_API_TOKEN=$3
  ACCESS_TOKEN=$4
fi


cd ~/daily-api
docker rm -f daily-api || true
docker build -t daily-api -f ./docker/api/Dockerfile .
docker run -d --name daily-api \
  -p 80:8080 \
  -e SPOTIFY_CLIENT_ID=$SPOTIFY_CLIENT_ID \
  -e SPOTIFY_CLIENT_SECRET=$SPOTIFY_CLIENT_SECRET \
  -e NOTION_API_TOKEN=$NOTION_API_TOKEN \
  -e ACCESS_TOKEN=$ACCESS_TOKEN \
  daily-api
