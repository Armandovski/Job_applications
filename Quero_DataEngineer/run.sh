#!/bin/bash

if [[ $1 == "fclean" ]];
then
    docker rm $(docker ps -qa) -f
    docker rmi quero
fi

if [[ $1 == "new" ]];
then
    docker build -t quero .
    docker run --name quero_cont -it quero
fi

docker start quero_cont