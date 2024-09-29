#!/bin/bash
# Script to backup data volume for Velo Supervisor 2000

set -o xtrace

rm -vf /home/pi/backup/velo-supervisor-2000.tar
docker container stop velo-supervisor-2000
sleep 5
docker run --rm --volumes-from velo-supervisor-2000 -v /home/pi/backup:/backup ubuntu tar cvf /backup/velo-supervisor-2000.tar /data 
docker container start velo-supervisor-2000

#For more information, see https://docs.docker.com/storage/volumes/#back-up-restore-or-migrate-data-volumes