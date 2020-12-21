CREATE USER 'data_engineer' WITH CREATEDB data_engineer
ALTER ROLE data_engineer WITH PASSWORD 'quero_educacao';
CREATE DATABASE data_engineer;
GRANT ALL PRIVILEGES ON DATABASE data_engineer TO data_engineer;
\q