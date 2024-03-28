#!/bin/bash

docker-compose down

IMAGE_ID_backend=$(docker images -q tele-meet-bot-backend)

if [ -n "$IMAGE_ID_backend" ]; then
    docker rmi -f $IMAGE_ID_backend
fi

#docker-compose up -d
docker-compose up
