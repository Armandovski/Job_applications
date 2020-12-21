# ************************************ #
# Created on Sun Dec 20 09:05:53 2020
#
# @author: Armando Alvarez Rolins
#
# @title: Dockerfile
# ************************************ #

# Select image from Dockerhub
FROM ubuntu:latest


# Run installation non-interactively (faster)
ARG DEBIAN_FRONTEND=noninteractive

# Copy and past the scrs folder to container root
COPY srcs /root/

# Install updates and tools
RUN apt-get update && apt -y upgrade && \
	apt-get install -y python3-dev python3-pip python3-psycopg2 postgresql-12 sudo && \
	apt -y install postgresql postgresql-contrib && \
	pip3 install requests pandas termcolor && \
	echo "fsync = off" >> /etc/postgresql/12/main/postgresql.conf && \
	echo "data_sync_retry = true" >> /etc/postgresql/12/main/postgresql.conf

ENTRYPOINT bash /root/start.sh