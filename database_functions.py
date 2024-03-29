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


def in_table(conn, cur, table, column, page_id):
	sql = f"""SELECT EXISTS(SELECT 1 FROM {table} WHERE {column} = '{page_id}')"""
	try:
		cur.execute(sql)
		return cur.fetchone()[0]
	except (Exception, psycopg2.DatabaseError) as error:
		print (error)
		return None


def insert_row_links(conn, cur, page_id, links):

	'''
	Adds new row to links table: [page_id][links]
	'''

	sql = f"""INSERT INTO links(page_id, page_links) VALUES(%s, %s)"""
	try:
		cur.execute(sql, (page_id, links,))
		conn.commit()
	except (Exception, psycopg2.DatabaseError) as error:
		print (error)


def add_link(conn, cur, page_id, link):

	'''
	Appends new link to current string for page_id
	'''

	if not in_table(conn, cur, "links", "page_id", page_id):
		sql = f"""INSERT INTO links(page_id, page_links) VALUES(%s, %s)"""
		try:
			cur.execute(sql, (page_id, link,))
			conn.commit()
		except (Exception, psycopg2.DatabaseError) as error:
			print (error)
		return

	sql = f"""UPDATE links SET page_links = '{link}|' || page_links WHERE page_id = '{page_id}'"""
	try:
		cur.execute(sql)
		conn.commit()
	except (Exception, psycopg2.DatabaseError) as error:
		print (error)


def insert_row_info(conn, cur, page_id, page_name, is_redirect):

	'''
	Adds new row to info table: [page_id][page_name]
	'''

	sql = f"""INSERT INTO info(page_id, page_name, is_redirect) VALUES(%s, %s, %s)"""
	try:
		cur.execute(sql, (page_id, page_name, is_redirect,))
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


def get_database_id(conn, cur, page_name):
	sql = f"""SELECT page_id FROM info WHERE page_name = '{page_name}'"""
	try:
		cur.execute(sql)
		name = cur.fetchone()
		return name
	except (Exception, psycopg2.DatabaseError) as error:
		print (error)
		return None


'''
if __name__ == '__main__':

'''