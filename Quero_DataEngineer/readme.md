# PostgreSQL Installation & Setup
Install PostgreSQL using Psql CLI client
```Shell
sudo apt update
sudo apt-get install postgresql-12
sudo apt install postgresql postgresql-contrib
```

To start the server
```Shell
sudo service postgresql start
sudo -u postgres createuser "username"
sudo -u postgres createdb "username"
```
For example ```"username" = 'data_engineer'```. PostgreSQL default is to have a database with the same name as the user

Use ```sudo -u postgres psql``` to login as superuser

It may be necessary to add the following lines at the end of the file postgresql.conf
```
fsync = off
data_sync_retry = true
```
The file can be found at ```/etc/postgresql/12/main/postgresql.conf```

Set user password:
```SQL
postgres=# ALTER ROLE username WITH PASSWORD 'password';
```
For this case the ```username``` has been set to ```data_engineer``` and ```'password'``` to ```'quero_educacao'```

## Install Psycopg2

```Shell
sudo apt-get install -y python3-psycopg2
```