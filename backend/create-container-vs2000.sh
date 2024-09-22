#!/bin/bash

set -o xtrace

# Clean up current container and image
docker container stop send-strava
docker container rm send-strava
docker image rm send-strava

# Get latest version number


# Build the image and tag it
docker build -t send-strava -f send-strava.Dockerfile .

# Create the container
docker run -d \
  --name=send-strava \
  -e TZ=Europe/Stockholm \
  -v /home/pi/code/secrets:/secrets \
  --restart unless-stopped \
  send-strava \
  ./send_strava.py \
  --oauth_file /secrets/strava_tokens.json \
  --mqtt_host messagebroker \
  --mqtt_port 1883 \
  --mqtt_topic strava \
  --mqtt_client_id send-strava