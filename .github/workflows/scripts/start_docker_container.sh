#!/bin/bash
set -e

cd ~/spotify-api
docker rm -f spotify-api || true
docker build -t spotify-api -f ./docker/api/Dockerfile .
docker run -d --name spotify-api \
  -p 80:8080 \
  -e SPOTIFY_CLIENT_ID=$SPOTIFY_CLIENT_ID \
  -e SPOTIFY_CLIENT_SECRET=$SPOTIFY_CLIENT_SECRET \
  spotify-api
