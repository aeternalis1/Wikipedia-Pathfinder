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
		"""
		CREATE TABLE """ + title + """ (
			link_name VARCHAR(255) NOT NULL
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
		print (error)
	finally:
		if conn is not None:
			conn.close()


def populate_table(title, links):
	sql = """INSERT INTO """ + title + """(link_name) VALUES(%s)"""
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		cur = conn.cursor()
		cur.executemany(sql, links)
		conn.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print (error)
	finally:
		if conn is not None:
			conn.close()


def get_database_links(title):
	sql = """SELECT link_name FROM """ + title + """ ORDER BY link_name"""
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		cur = conn.cursor()
		cur.execute(sql)
		print ("The number of parts:", cur.rowcount)
		rows = cur.fetchall()
		for row in rows:
			print (row)
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print (error)
	finally:
		if conn is not None:
			conn.close()


if __name__ == '__main__':
	#create_table('King_Duncan')
	#populate_table('King_Duncan', [('Macbeth',), ('Shakespeare',), ('Banquo',), ('Scotland',)])
	get_database_links('King_Duncan')