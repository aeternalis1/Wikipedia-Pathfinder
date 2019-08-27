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


def create_table(title):
	sql = (
		f"""
		CREATE TABLE {title} (
			index SERIAL PRIMARY KEY,
			page_id VARCHAR(255) NOT NULL,
			page_name VARCHAR(255) NOT NULL
		)
		"""
        )
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		cur = conn.cursor()
		cur.execute(sql, (title,))
		cur.close()
		conn.commit()
	except (Exception, psycopg2.DatabaseError) as error:
		# print (error)
		if conn is not None:
			conn.close()
		raise error
	finally:
		if conn is not None:
			conn.close()


def populate_table(title, ids, titles):
	sql = f"""INSERT INTO {title}(page_id, page_name) VALUES(%s, %s)"""
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		cur = conn.cursor()
		cur.executemany(sql, [(i, j,) for i, j in zip(ids, titles)])
		conn.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		# print (error)
		raise error
	finally:
		if conn is not None:
			conn.close()


def get_database_links(title):
	sql = f"""SELECT page_id, page_name FROM {title} ORDER BY index"""
	conn = None
	page_ids = None
	page_names = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		cur = conn.cursor()
		cur.execute(sql)
		# print ("The number of parts:", cur.rowcount)
		rows = cur.fetchall()
		page_ids = [row[0] for row in rows]
		page_names = [row[1] for row in rows]
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		# print (error)
		if conn is not None:
			conn.close()
		raise error
	finally:
		if conn is not None:
			conn.close()
	return page_ids, page_names

'''
if __name__ == '__main__':
	#create_table('King_Duncan')
	#populate_table('King_Duncan', [('Macbeth',), ('Shakespeare',), ('Banquo',), ('Scotland',)])
	#get_database_links('King_Duncan')
	create_table('p_1')
	populate_table('p_1', ['1', '2', '3'], ['a', 'b', 'c'])
'''