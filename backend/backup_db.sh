#!/bin/bash
# Script to backup data volume for Velo Supervisor 2000

set -o xtrace

rm -vf /home/pi/backup/nodered.tar
docker container stop nodered
sleep 5
docker run --rm --volumes-from nodered -v /home/pi/backup:/backup ubuntu tar cvf /backup/nodered.tar /data 
docker container start nodered

#For more information, see https://docs.docker.com/storage/volumes/#back-up-restore-or-migrate-data-volumes