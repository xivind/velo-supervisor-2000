#!/bin/bash
# Script to backup database for Velo Supervisor 2000

set -o xtrace

docker container stop velo-supervisor-2000
sleep 5
rm -vf /home/pi/backup/prod_db.sqlite
cp /home/pi/code/container_data/prod_db.sqlite /home/pi/backup/prod_db.sqlite
docker container start velo-supervisor-2000

