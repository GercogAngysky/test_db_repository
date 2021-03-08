import sqlite3 as sq
import example


def create_connection(db):
	try:
		connection = sq.connect(db)
		print("Connection to SQLite DB successful")
	except sq.Error as error:
		print(f"The error '{error}' occurred")
	finally:
		return connection or None


def execute_select_query(connection, query: list):
	cursor = connection.cursor()
	try:
		cursor.execute("""PRAGMA foreign_keys = ON;""")
		cursor.execute(*query)
		print("Query select executed successfully")
	except sq.Error as error:
		print(f"The error '{error}' occurred")
	finally:
		return cursor.fetchall()


def execute_insert_query(connection, query: list):
	cursor = connection.cursor()
	try:
		cursor.execute("""PRAGMA foreign_keys = ON;""")
		cursor.execute("""BEGIN;""")
		cursor.execute(*query)
		connection.commit()
		print("Query insert executed successfully")
	except sq.Error as error:
		print(f"The error '{error}' occurred")
		if connection:
			connection.rollback()
	finally:
		return cursor.lastrowid



def create_insert_query(tablename, data) -> list:
	return [ f""" INSERT INTO {tablename} {tuple(data.keys())} VALUES ({",".join("?" for i in data)} );""",	list(data.values()) ]


# функция принимает имя таблицы, словарь {атрибут: значение} c известными данными и 
# список имен атрибутов, значения которых нужно найти, возвращает строку SQL-запроса 
def create_query_find_values( table, known_attr_values: dict, find_values_on_attr: list ) -> list:
	find_attr = ', '.join( [attr for attr in find_values_on_attr] )
	known_attr = ' AND '.join( [f"{attr} == '{val}'" for attr, val in known_attr_values.items()] )
	res = f"""
		SELECT
			{find_attr}
		FROM
			{table}
		WHERE
			{known_attr}
		"""
	return [res]


def input_values_for_table(tablename) -> dict:
	data = {}
	for key in example.tables[tablename]:	
		value = input(f"{key:>14}:  ")
		data[key] = value
	return data


def add_client(database, table, client: dict):
	connect = create_connection(database)
	query = create_insert_query(table, client) # создать строку запроса
	_id_ = execute_insert_query(connect, query)  # выполнить запрос
	try:
		if _id_:
			print('новый клиент добавлен, _id_ = ', _id_)
			connect.close()
			return _id_
		else:
			data = {
					'family': client['family'],
					  'name': client['name'],
				'patronymic': client['patronymic']
			}
			query = create_query_find_values(table, data, ['_id_']) # создать строку запроса
			_id_ = execute_select_query( connect, query )           # выполнить запрос
			if _id_:
				print('такая запись уже есть, _id_ = ', _id_[0][0])
				connect.close()
				return _id_[0][0]
			else:
				print('запись не добавлена')
				connect.close()
	except:
		connect.close()
		print('возникла ошибка')



# порядок записи в таблицы: clients -> adress -> contracts -> products

db = 'test.db'

#new_client = input_values_for_table('clients')

new_client = {
			'family': 'Баженов',
	          'name': 'Евгений',
	    'patronymic': 'Александрович',
	 'date_of_birth': '1988-11-25',
	  'passport_ID_': '42492542',
	'phone_number_1': '8888888',
	'phone_number_2': '9999999'
}



add_client(db, 'clients', new_client)
				








input()