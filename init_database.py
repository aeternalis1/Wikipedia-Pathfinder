from config import config
import psycopg2


def create_links_table():
	sql = (
		f"""
		CREATE TABLE links (
			page_id VARCHAR(255) PRIMARY KEY,
			page_links text NOT NULL
		)
		"""
        )
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		cur = conn.cursor()
		cur.execute(sql)
		cur.close()
		conn.commit()
	except (Exception, psycopg2.DatabaseError) as error:
		print (error)
	finally:
		if conn is not None:
			conn.close()


def create_info_table():
	sql = (
		f"""
		CREATE TABLE info (
			page_id VARCHAR(255) PRIMARY KEY,
			page_name text NOT NULL
		)
		"""
        )
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		cur = conn.cursor()
		cur.execute(sql)
		cur.close()
		conn.commit()
	except (Exception, psycopg2.DatabaseError) as error:
		print (error)
	finally:
		if conn is not None:
			conn.close()


'''
if __name__ == '__main__':
	pass
'''