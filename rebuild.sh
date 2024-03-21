#!/bin/bash

docker-compose down

IMAGE_ID=$(docker images -q python-dockerfile)

if [ -n "$IMAGE_ID" ]; then
    docker rmi -f $IMAGE_ID
fi

docker build -t python-dockerfile .
docker-compose up -d
