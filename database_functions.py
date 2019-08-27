from config import config
import psycopg2


def connect():
	conn = None
	try:
		params = config()
		conn = psycopg2.connect(**params)
		cur = conn.cursor()
		return conn, cur
	except (Exception, psycopg2.DatabaseError) as error:
		print (error)
		return None, None


def insert_row_links(conn, cur, page_id, links):
	sql = f"""INSERT INTO links(page_id, page_links) VALUES(%s, %s)"""
	try:
		cur.execute(sql, (page_id, links,))
		conn.commit()
	except (Exception, psycopg2.DatabaseError) as error:
		print (error)


def insert_row_info(conn, cur, page_id, page_name):
	sql = f"""INSERT INTO info(page_id, page_name) VALUES(%s, %s)"""
	try:
		cur.execute(sql, (page_id, page_name,))
		conn.commit()
	except (Exception, psycopg2.DatabaseError) as error:
		print (error)


def get_database_links(conn, cur, page_id):
	sql = f"""SELECT page_links FROM links WHERE page_id = '{page_id}'"""
	try:
		cur.execute(sql)
		links = cur.fetchone()
		return links[0].split('|')
	except (Exception, psycopg2.DatabaseError) as error:
		print (error)
		return None


def get_database_info(conn, cur, page_id):
	sql = f"""SELECT page_name FROM info WHERE page_id = '{page_id}'"""
	try:
		cur.execute(sql)
		name = cur.fetchone()
		return name
	except (Exception, psycopg2.DatabaseError) as error:
		print (error)
		return None


def in_table(conn, cur, table, page_id):
	sql = f"""SELECT EXISTS(SELECT 1 FROM {table} WHERE page_id = '{page_id}')"""
	try:
		cur.execute(sql)
		return cur.fetchone()[0]
	except (Exception, psycopg2.DatabaseError) as error:
		print (error)
		return None

'''
if __name__ == '__main__':

'''