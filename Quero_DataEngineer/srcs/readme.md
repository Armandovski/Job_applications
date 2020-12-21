# Quero Educação - Data Engineer Job Application
Hard skills exercise for the application process to a Data Engineer position.
I was asked to extract data from their API and load it to a PostgreSQL table.

The following sets up a container to host a local PostgreSQL server and a python
script which performs the Extract, Transform, and Load (ETL) of the data.
The python script checks if a file called ```input``` exists in it's directory.
If it does not, it pulls the data from the provided API and loads it to the file
with the given name, if the file already exists it just reads the data locally.

It treats the data and loads it to a PostgreSQL table. Since it is stated in the
assignment that the data is public, the table is set-up in the default public
schema, with a generic user called ```data_engineer``` with all privileges to
the database.

NOTE: If the script is run outside of a container, skip the Build Instructions.

## Contents
```@root```
- Dockerfile - instructions for building the docker image and required installs
- run.sh - script to setup, start or clean container

```@/srcs```
- start.sh - PostgreSQL server start
- setup.sh - script to setup installations and configurations as required
- main.py - main script with performs ETL process
- setup_sql - ---NOT IN USE---

## Build Instructions
The following instructions are for setting up the pipeline in a docker container.
Run the following script to initiate setup:
```bash run.sh new```
This script should make a build and image called ```quero``` and create a container
called ```quero_cont```
It will open the bash CLI for the container.

### PostgreSQL Installation & Setup
The PostgreSQL setup needs to be performed at the bash CLI of the container. It
will already have the PostgreSQL server started.
Enter the PostgreSQL server as the superuser as follows:
```sudo -u postgres psql```
This will lead into a SQL CLI. Create a user, password and database as follows:
```SQL
CREATE USER data_engineer WITH PASSWORD 'quero_educacao;
CREATE DATABASE data_engineer;
GRANT ALL PRIVILEGES ON DATABASE data_engineer TO data_engineer;
```
Use ```\q``` to exit postgres.

### Run ETL
Run the pipeline with the following command:
```Shell
python3 root/main.py
```
