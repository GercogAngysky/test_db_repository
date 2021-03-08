import sqlite3 as sq
import example  

def create_connection(path):
	connection = None
	try:
		connection = sq.connect(path)
		print("Connection to SQLite DB successful")
	except sq.Error as error:
		print(f"The error '{error}' occurred")
	return connection


def execute_query(connection, query):
	cursor = connection.cursor()
	try:
		cursor.execute("""PRAGMA foreign_keys = ON;""")
		cursor.execute("""BEGIN;""")
		cursor.execute(*query)
		connection.commit()
		print("Query executed successfully")
	except sq.Error as error:
		print(f"The error '{error}' occurred")
		if connection:
			connection.rollback()
	connection.close()


def execute_read_query(connection, query):
	cursor = connection.cursor()
	try:
		cursor.execute("""PRAGMA foreign_keys = ON;""")
		cursor.execute(query)
		connection.commit()
		return cursor.fetchall()
	except sq.Error as e:
		print(f"The error '{e}' occurred")
	connection.close()


# формирует список [запрос, данные]
def create_insert_row(tablename, data):
	return [ f""" INSERT INTO {tablename} {tuple(data.keys())} VALUES ({",".join("?" for i in data)} );""",	list(data.values()) ]


create_clients_table = ["""
		CREATE TABLE IF NOT EXISTS 'clients' (
			'_id_' INTEGER PRIMARY KEY AUTOINCREMENT,
			'family' TEXT NOT NULL,
			'name' TEXT NOT NULL,
			'patronymic' TEXT NOT NULL,
			'date_of_birth' TEXT,
			'passport_ID_' TEXT UNIQUE NOT NULL,
			'phone_number_1' TEXT NOT NULL,
			'phone_number_2' TEXT,
		UNIQUE ('family', 'name', 'patronymic')
			);
			"""]

create_adress_table = ["""
		CREATE TABLE IF NOT EXISTS 'adress' (
			'_id_' INTEGER PRIMARY KEY AUTOINCREMENT,
			'city' TEXT NOT NULL DEFAULT 'Ноябрьск',
			'street' TEXT NOT NULL,
			'house' TEXT NOT NULL,
			'apartment' TEXT NOT NULL,
			'porch' TEXT,
			'floor' TEXT,
		UNIQUE ('city', 'street', 'house', 'apartment')
			);
			"""]

create_contracts_table = ["""
		CREATE TABLE IF NOT EXISTS 'contracts' (
			'_id_' INTEGER PRIMARY KEY AUTOINCREMENT,
			'number' TEXT NOT NULL,
			'date' TEXT NOT NULL,
			'clients_id_' TEXT NOT NULL,
			'adress_id_' INTEGER NOT NULL,
		UNIQUE ('number', 'date')
		FOREIGN KEY ('clients_id_') REFERENCES clients('_id_'),
		FOREIGN KEY ('adress_id_') REFERENCES adress('_id_')
			);
			"""]

create_products_table = ["""
		CREATE TABLE IF NOT EXISTS 'products' (
			'_id_' INTEGER PRIMARY KEY AUTOINCREMENT,
			'name' TEXT NOT NULL,
			'count' INTEGER NOT NULL DEFAULT 1,
			'price' REAL NOT NULL,
			'contracts_id_' INTEGER NOT NULL,
		UNIQUE ('name', 'price', 'contracts_id_'),
		FOREIGN KEY ('contracts_id_') REFERENCES contracts('_id_')
			);
			"""]

create_makers_table = ["""
		CREATE TABLE IF NOT EXISTS 'makers' (
			'_id_' INTEGER PRIMARY KEY AUTOINCREMENT,
			'name' TEXT UNIQUE,
			'adress' TEXT,
			'manager' TEXT,
			'phone' TEXT
			);
			"""]

create_orders_table = ["""
		CREATE TABLE IF NOT EXISTS 'orders' (
			'_id_' INTEGER PRIMARY KEY AUTOINCREMENT,
			'date' TEXT NOT NULL,
			'products_id_' INTEGER NOT NULL,
			'makers_id_' INTEGER NOT NULL,
		UNIQUE ('date', 'products_id_', 'makers_id_' )
			);
			"""]


db = 'test.db'

execute_query( create_connection(db), create_clients_table )
execute_query( create_connection(db), create_adress_table )
execute_query( create_connection(db), create_contracts_table )
execute_query( create_connection(db), create_products_table )
execute_query( create_connection(db), create_makers_table )
execute_query( create_connection(db), create_orders_table )



# строка запроса для создания новой записи в таблицу, формируется в функции create_insert_row
insert_clients = """
		INSERT
			clients(name','patronymic', 'date_of_birth', 'passport_ID_', 'phone_number_1', phone_number_2')
		VALUES
			('Ласунова', 'Наталья', 'Александровна', '1965-07-04', '74086569191', '89124235335', '')		
		"""

execute_query( create_connection(db), create_insert_row('clients', example.tables['clients']) )
execute_query( create_connection(db), create_insert_row('adress', example.tables['adress']) )
execute_query( create_connection(db), create_insert_row('contracts', example.tables['contracts']) )
execute_query( create_connection(db), create_insert_row('products', example.tables['products']) )


select_clients = """
		SELECT
			clients.name,
			adress.street,
			adress.house,
			contracts.number,
			products.name,
			products.price
		FROM
			contracts
		INNER JOIN clients ON clients._id_ = contracts.clients_id_
		INNER JOIN adress ON adress._id_ = contracts.adress_id_
		INNER JOIN products ON products.contracts_id_ = contracts._id_
		"""

print(execute_read_query( create_connection(db), select_clients ))


update_price = ["""
		UPDATE
			products
		SET
			price = 55000
		WHERE
			_id_ = 1
		"""]

execute_query( create_connection(db), update_price )
print(execute_read_query( create_connection(db), select_clients ))

delete_product = ["""
		DELETE FROM
			products
		WHERE
			_id_ = 1
		"""]

#execute_query( create_connection(db), delete_product )
#print(execute_read_query( create_connection(db), select_clients ))


# получаетм дату в форамте: YYYY-MM-DD
# str(sq.datetime.date.today())

input()