from config import config
import psycopg2


def connect():
	conn = None
	try:
		params = config()
		print ('Connecting to PostgreSQL database...')
		conn = psycopg2.connect(**params)

		cur = conn.cursor()
		print ('PostgreSQL database version:')
		cur.execute('SELECT version()')

		db_version = cur.fetchone()
		print (db_version)
	except (Exception, psycopg2.DatabaseError) as error:
		print (error)
	finally:
		if conn is not None:
			conn.close()
			print ('Database connection closed.')


def create_tables():
	commands = (
		"""
		CREATE TABLE vendors (
			vendor_id SERIAL PRIMARY KEY,
			vendor_name VARCHAR(255) NOT NULL
		)
		""",
		"""
		CREATE TABLE parts (
				part_id SERIAL PRIMARY KEY,
				part_name VARCHAR(255) NOT NULL
				)
		""",
		"""
		CREATE TABLE part_drawings(
				part_id INTEGER PRIMARY KEY,
				file_extension VARCHAR(5) NOT NULL,
				drawing_data BYTEA NOT NULL,
				FOREIGN KEY (part_id)
				REFERENCES parts (part_id)
				ON UPDATE CASCADE ON DELETE CASCADE
		)
		""",
		"""
        CREATE TABLE vendor_parts (
                vendor_id INTEGER NOT NULL,
                part_id INTEGER NOT NULL,
                PRIMARY KEY (vendor_id , part_id),
                FOREIGN KEY (vendor_id)
                    REFERENCES vendors (vendor_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (part_id)
                    REFERENCES parts (part_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
        )
        """
        )
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		cur = conn.cursor()
		for command in commands:
			cur.execute(command)
		cur.close()
		conn.commit()
	except (Exception, psycopg2.DatabaseError) as error:
		print (error)
	finally:
		if conn is not None:
			conn.close()


def insert_vendor(vendor_name):
	sql = """INSERT INTO vendors(vendor_name) VALUES(%s) RETURNING vendor_id;"""
	conn = None
	vendor_id = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		cur = conn.cursor()
		cur.execute(sql, (vendor_name,))
		vendor_id = cur.fetchone()[0]
		conn.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print (error)
	finally:
		if conn is not None:
			conn.close()

	return vendor_id


def insert_vendor_list(vendor_list):
	sql = """INSERT INTO vendors(vendor_name) VALUES(%s)"""
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		cur = conn.cursor()
		cur.executemany(sql, vendor_list)
		conn.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print (error)
	finally:
		if conn is not None:
			conn.close()


def update_vendor(vendor_id, vendor_name):
	sql = """UPDATE vendors 
			SET vendor_name = %s 
			WHERE vendor_id = %s"""
	conn = None
	updated_rows = 0
	try:
		params = config()
		conn = psycopg2.connect(**params)
		cur = conn.cursor()
		cur.execute(sql, (vendor_name, vendor_id))
		updated_rows = cur.rowcount
		conn.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print (error)
	finally:
		if conn is not None:
			conn.close()

	return updated_rows


def get_vendors():
	sql = """SELECT vendor_id, vendor_name FROM vendors WHERE vendor_name = '3M Corporation'"""
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		cur = conn.cursor()
		cur.execute(sql)
		print ("The number of parts:", cur.rowcount)
		row = cur.fetchone()
		while row is not None:
			print (row)
			row = cur.fetchone()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print (error)
	finally:
		if conn is not None:
			conn.close()


if __name__ == '__main__':
	get_vendors()
	#update_vendor(1, "3M Corporation")
	'''insert_vendor("3M Co.")
	insert_vendor_list([
		('AKM Semiconductor Inc.',),
		('Asahi Glass Co Ltd.',),
		('Daikin Industries Ltd.',),
		('Blah blah blah',)
	])'''
