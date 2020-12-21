# ************************************ #
# Created on Sun Dec 20 09:05:53 2020
#
# @author: Armando Alvarez Rolins
#
# @title: setup.sh
# ************************************ #

#!/bin/bash

## POSTGRESQL SETUP

# Add settings to configuration file
sudo echo "fsync = off" >> /etc/postgresql/12/main/postgresql.conf
sudo echo "data_sync_retry = true" >> /etc/postgresql/12/main/postgresql.conf

# Start Server
service postgresql start
sudo -u postgres psql