from query_api import *
from database_functions import *
from helper import get_page_title, get_page_id
import time


def get_edges(title):
	try:
		ids, names = get_database_links(title)
		return ids, names
	except:
		return None, None


def bfs(source, target):			# string, string
	print (f"Finding path from {source} to {target}.")
	start_time = time.time()

	source_id = get_page_id(source)
	target_id = get_page_id(target)

	queue = [[source_id, source]]

	visited = {source_id: 1}			# map string to bool, seen or not
	backedge = {source: None}			# stores a list of pages that lead to [page]

	found = 0
	while not found:

		new_queue = []

		while queue:
			cur_id, cur_name = queue.pop(0)

			page_ids, page_names = get_edges('p_' + cur_id)	# table names must start w/ letter

			if page_ids == None:
				page_ids, page_names = gen_links(cur_id)
				create_table('p_' + cur_id)
				populate_table('p_' + cur_id, page_ids, page_names)
			

			for page_id, page_name in zip(page_ids, page_names):
				if page_id in visited:
					continue
				if page_id not in backedge:
					new_queue.append([page_id, page_name])
					backedge[page_name] = [cur_name]
				else:
					backedge[page_name].append(cur_name)

		for i in new_queue:
			visited[i[0]] = 1
			if i[0] == target_id:
				found = 1

		queue = new_queue

	path = [target]
	while backedge[target] != None:
		page = backedge[target][0]
		path.append(page)
		target = page

	total_time = time.time()-start_time
	print ("Completed in %.2f seconds." % total_time)

	return path[::-1]


#print (get_edges('King_Duncans'))
#print (bfs('Algorithm', 'Donald Trump'))
print (bfs('King Duncan', 'Scotland'))

'''

keep a database of articles and the links to and from that page
whenever a new article is encountered, just store get_links(cur) in database
when an article was previously seen, just get the links from the database

can query links from several pages at once (e.g. "King Duncan|Jimmie|Mathematics")
	- differing origin page can be determined via alphabetical order of results?

'''