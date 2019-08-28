from query_api import *
from database_functions import *
from helper import get_page_title, get_page_id
import time


def get_edges(conn, cur, title):
	try:
		links = get_database_links(conn, cur, title)
		return links
	except:
		return None


def get_paths(target_id, parent):
	paths = [[target_id]]
	while parent[paths[0][-1]] != None:
		new_paths = []
		for path in paths:
			for edge in parent[path[-1]]:
				new_paths.append(path+[edge])
		paths = new_paths
	return [path[::-1] for path in paths]


def bfs(source, target):			# string, string
	conn, cur = connect()
	print (f"Finding path from {source} to {target}.")
	start_time = time.time()

	source_id = get_page_id(source)
	target_id = get_page_id(target)

	if not in_table(conn, cur, 'info', source_id):
		insert_row_info(conn, cur, source_id, source)

	queue = [source_id]

	visited = {source_id: 1}			# map string to bool, seen or not
	backedge = {source_id: None}		# stores a list of pages that lead to [page]

	found = 0
	while not found:

		new_queue = []

		while queue:
			cur_id = queue.pop(0)

			'''
			if current page is not in the database, query the Wikipedia API and
			dynamically add it to the database.
			'''

			if in_table(conn, cur, 'links', cur_id):
				page_ids = get_edges(conn, cur, cur_id)
			else:
				page_ids, page_names = gen_links(cur_id)
				insert_row_links(conn, cur, cur_id, '|'.join(page_ids))
				for page_id, page_name in zip(page_ids, page_names):
					if not in_table(conn, cur, 'info', page_id):
						insert_row_info(conn, cur, page_id, page_name)

			for page_id in page_ids:
				if page_id in visited:
					continue
				if page_id not in backedge:
					new_queue.append(page_id)
					backedge[page_id] = [cur_id]
				else:
					backedge[page_id].append(cur_id)

		for i in new_queue:
			visited[i] = 1
			if i == target_id:
				found = 1

		queue = new_queue

	'''
	path = [target_id]
	while backedge[target_id] != None:
		page = backedge[target_id][0]
		path.append(page)
		target_id = page
	'''	
	total_time = time.time()-start_time
	print ("Completed in %.2f seconds." % total_time)

	paths = get_paths(target_id, backedge)
	count, degree = len(paths), len(paths[0])-1
	paths = [" -> ".join([get_database_info(conn, cur, page_id)[0] for page_id in path]) for path in paths]

	return ["%d paths of %d degree(s) of separation were found:" % (count, degree)] + paths


#print (bfs('Adolf Hitler', 'Post Malone'))

'''

keep a database of articles and the links to and from that page
whenever a new article is encountered, just store get_links(cur) in database
when an article was previously seen, just get the links from the database


apparently postgres has unlimited rows per table:
time to fricking change everything again

'''