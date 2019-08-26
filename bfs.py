from query_api import *


def bfs(source, target):			# string, string
	queue = [source]

	visited = {source: 1}			# map string to bool, seen or not
	backedge = {source: None}		# stores a list of pages that lead to [page]

	while target not in queue:

		new_queue = []

		while queue:
			query = "|".join(queue[:min(50, len(queue))])

			try:
				links = sorted(get_links(query))
			except:	
				continue		# invalid link (NEEDS CHANGING! one bad link throws out the whole batch)
								# might need to use gen_links instead of get_links

			for i in range(len(links)):
				if int(links[i][0]) <= 0:	# invalid id
					continue
				if links[i][1] in visited:
					continue
				if links[i][1] not in backedge:
					new_queue.append(links[i][1])
					backedge[links[i][1]] = [links[i][0]]
				else:
					backedge[links[i][1]].append(links[i][0])

		for i in new_queue:
			visited[i] = 1
		queue = new_queue

	path = [target]
	while backedge[target] != None:
		page = get_page_title(backedge[target][0])
		path.append(page)
		target = page

	return path[::-1]


print (bfs('Jimmie', '1964 World Series'))


'''

keep a database of articles and the links to and from that page
whenever a new article is encountered, just store get_links(cur) in database
when an article was previously seen, just get the links from the database

can query links from several pages at once (e.g. "King Duncan|Jimmie|Mathematics")
	- differing origin page can be determined via alphabetical order of results?

'''