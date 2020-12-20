import sys
import os.path
import requests
import json
import pandas as pd
import psycopg2
from psycopg2 import Error
from io import StringIO
from termcolor import colored


def extract_data():
	'''
	This function checks if the input file exists in current directory. If not,
	it performs an html request to the API and writes to file. If it does, it
	reads from file.
	'''
	if not os.path.exists('./input'):
		with open("./input", "w") as f:
			r = requests.get("http://dataeng.quero.com:5000/caged-data")
			if r.status_code != 200:
				raise Exception("ERROR: Request failed")
			data = r.json()
			f.write(json.dumps(data))
	else:
		with open("./input") as f:
			 data = json.loads(f.read())

	if data['success'] == 'false':
		# TO DO: check if it's warning or error.
		print("WARNING: Data retrieved from API may be corrupt")
	return data['caged']


def connect_db(dict_conn_param):
	'''
	This function connects to the PostgreSQL database.
	'''
	try:
		connection = psycopg2.connect(**dict_conn_param)
		cursor = connection.cursor()
		print(colored("--- PostgreSQL server information ---", 'white', 'on_blue'))
		print(connection.get_dsn_parameters(), "\n")
		cursor.execute("SELECT version();")
		record = cursor.fetchone()
		print(colored("--- PostgreSQL Connection Established ---", 'white', 'on_green'))
		print(record, "\n")
	except (Exception, Error) as error:
		print(colored("ERROR: Could not connect to PostgreSQL", 'white', 'on_red'))
		print(error)
	return cursor, connection


def disconnect_db(cursor, connection):
	'''
	This function disconnects from the PostgreSQL database.
	'''
	if (connection):
		cursor.close()
		connection.close()
		print(colored("--- PostgreSQL Connection Closed ---", 'white', 'on_grey'))
	else:
		Exception(colored("ERROR: No connection to disconnect", 'white', 'on_red'))
	return


def df_to_SQL_stringio(connection, cursor, df, table):
	'''
	This function performs a bulk insert of the dataframe to SQL table using
	a file-like object (fastest way to insert large amounts of data).
	'''
	# Check if table exists already. If so, delete it.
	cursor.execute("SELECT EXISTS(select relname from pg_class where relname='{}')".format(table))
	if cursor.fetchone()[0]:
		cursor.execute("DROP TABLE {};".format(table))

	# Create table
	create_table(connection, cursor, df, table)

	# Save table in CSV format to an in-memory string buffer
	buffer = StringIO()
	df.to_csv(buffer, index=False, index_label='index', header=False, sep=',')
	buffer.seek(0)

	# Insert data to PostgreSQL table
	try:
		cursor.copy_expert("COPY {} FROM STDIN WITH (FORMAT CSV)".format(table), buffer)
		connection.commit()
		print(colored("Dataframe inserted to SQL table '{}' successfully!".format(table), 'green'))
		cursor.execute("SELECT * FROM {} WHERE id='{}'".format(table, 1))
		row = cursor.fetchone()
		colnames = [desc[0] for desc in cursor.description]
		print(colnames, row)
	except (Exception, Error) as error:
		print(colored("ERROR: {}".format(error), 'white', 'on_red'))


def create_table(connection, cursor, df, table):
	'''
	This function creates the table in PostgreSQL
	'''
	cursor.execute("CREATE TABLE {} (\
	id INTEGER PRIMARY KEY, \
	categoria INTEGER, \
	cbo2002_ocupacao INTEGER, \
	competencia INTEGER, \
	fonte INTEGER, \
	grau_de_instrucao INTEGER, \
	horas_contratuais INTEGER, \
	idade INTEGER, \
	ind_trab_intermitente INTEGER, \
	ind_trab_parcial INTEGER, \
	indicador_aprendiz INTEGER, \
	municipio INTEGER, \
	raca_cor INTEGER, \
	regiao INTEGER, \
	salario REAL, \
	saldo_movimentacao INTEGER, \
	secao VARCHAR(5), \
	sexo INTEGER, \
	subclasse INTEGER, \
	tam_estab_jan INTEGER, \
	tipo_de_deficiencia INTEGER, \
	tipo_empregador INTEGER, \
	tipo_estabelecimento INTEGER, \
	tipo_movimentacao INTEGER, uf INTEGER)"\
	.format(str(table)))

	cursor.execute("CREATE UNIQUE INDEX id ON {} USING btree (id);".format(table))
	return


def data_cleaning(df):
	'''
	This function is used to clean the data as required from the data exploration
	'''
	columns = [col for col in df.columns if col != 'id']
	columns.insert(0, 'id')
	df = df.reindex(columns=columns)
	df['salario'] = df['salario'].apply(lambda x: x.replace(',', ''))
	return df


def main():
	data = extract_data()

	# Convert JSON data to dataframe
	df = pd.DataFrame.from_dict(data)

	# Define PostgreSQL Params
	dict_conn_param = {
		"user" : 'data_engineer',
		"password" : 'quero_educacao',
		"host" : 'localhost',
		"database" : 'data_engineer'}

	# Clean dataframe
	df = data_cleaning(df)

	# Connect to PostgreSQL
	table = 'processo_seletivo'
	cursor, connection = connect_db(dict_conn_param)

	# Bulk insert the data frame to SQL
	df_to_SQL_stringio(connection, cursor, df, table)

	# Disconnect from PostgreSQL
	disconnect_db(cursor, connection)


if __name__ == '__main__':
	main()