#!/bin/bash

docker-compose down

IMAGE_ID_backend=$(docker images -q tele-meet-bot-backend)
if [ -n "$IMAGE_ID_backend" ]; then
    docker rmi -f $IMAGE_ID_backend
fi

IMAGE_ID_python=$(docker images -q python)
if [ -n "$IMAGE_ID_python" ]; then
    docker rmi -f $IMAGE_ID_python
fi

IMAGE_PGADMIN=$(docker images -q dpage/pgadmin4)
if [ -n "$IMAGE_PGADMIN" ]; then
    docker rmi -f $IMAGE_PGADMIN
fi

#docker-compose up -d
docker-compose up
