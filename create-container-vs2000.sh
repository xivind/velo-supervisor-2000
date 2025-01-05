#!/bin/bash

set -o xtrace

# Cleanup container and image
docker container stop velo-supervisor-2000
docker container rm velo-supervisor-2000
docker image rm velo-supervisor-2000

# Build and tag image
docker build -t velo-supervisor-2000 -f DOCKERFILE .

# Create and run container
docker run -d \
  --name=velo-supervisor-2000 \
  -e TZ=Europe/Stockholm \
  --mount type=bind,source=/home/pi/code/container_data,target=/data \
  --mount type=bind,source=/home/pi/code/secrets,target=/secrets \
  --restart unless-stopped \
  -p 8000:8000 \
  velo-supervisor-2000











 
