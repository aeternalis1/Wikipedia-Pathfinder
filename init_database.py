from config import config
from database_functions import insert_row_info, insert_row_links, connect
import psycopg2


def create_links_table():
	sql = (
		"""
		CREATE TABLE links (
			page_id INTEGER PRIMARY KEY,
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
		"""
		CREATE TABLE info (
			page_id INTEGER PRIMARY KEY,
			page_name VARCHAR(255) NOT NULL,
			is_redirect INTEGER NOT NULL
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
wikipedia sql dump's table format (columns):

0: page_id 	(int)
1: page_namespace (int)
2: page_title (varbinary)
3: page_restrictions (tinyblob)
4: page_is_redirect (tinyint)
5: page_is_new (tinyint)
6: page_random (double unsigned)
7: page_touched (varbinary)
8: page_links_updated (varbinary)
9: page_latest (int)
10: page_len (int)
11: page_content_model (varbinary)
12: page_lang (varbinary)

e.g.
(10,0,'AccessibleComputing','',1,0,0.33167112649574004,'20190728220305',
'20190105021557',854851586,94,'wikitext',NULL)

page_title is a piece of crap. it can contain commas, apostrophes and brackets

plan:
ignore commas if nested within quotes
ignore closing quote unless directly before comma
ignore opening quote unless directly after comma

page_title for comma is: page_id,',',page_restrictions

apparently ',' is a page title (redirects to 44).

THIS CAN BE RESOLVED BY GETTING EVERYTHING BEFORE AND EVERYTHING BEHIND THE TITLE

Find end of pageinfo by searching for string `,NULL)`

'''


def populate_info_database(conn, cur):
	file = "c:/wikipedia/enwiki-latest-page.sql"
	f = open(file, "r", encoding="utf8")
	if f.mode != "r":
		print ("Error: file not opened.")
		return

	line = f.readline()
	v = 0
	while line:
		if 'INSERT INTO' in line:
			length = len(line)
			ind = 0
			while ind < length and line[ind] != '(':
				ind += 1
			stack = []
			commas = 0
			while ind < length:
				stack.append(line[ind])
				if line[ind] == ',':
					commas += 1
				if line[ind] == ')' and commas > 10:	# no way there's an article with 8+ commas and a )
					arr = []
					arr2 = []
					commas = 0
					temp = []

					for i in range(1,len(stack)):
						if stack[i] == ',':
							arr.append("".join(temp))
							temp = []
						else:
							temp.append(stack[i])
						if len(arr) == 2:
							left_ind = i
							break

					for i in range(len(stack)-2,-1,-1):	# count 10 commas back to title
						if stack[i] == ',':
							arr2.insert(0, "".join(temp))
							temp = []
						else:
							temp.insert(0, stack[i])
						if len(arr2) == 10:
							right_ind = i
							break

					arr = arr + [''.join(stack[left_ind+1:right_ind])] + arr2
					for i in range(len(arr)):
						arr[i] = arr[i].strip('\'')

					if arr[1] == '0':
						insert_row_info(conn, cur, int(arr[0]), arr[2].strip('\''), int(arr[4]=='1'))

					ind += 1
					stack = []
					commas = 0

				ind += 1

		line = f.readline()



def populate_links_database():
	file = "c:/wikipedia/enwiki-latest-pagelinks.sql"



if __name__ == '__main__':
	#create_info_table()
	conn, cur = connect()
	populate_info_database(conn, cur)