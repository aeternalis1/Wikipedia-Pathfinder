from query_api import *

def bfs(source, target):
	queue = [source]

	visited = {source: 1}

	while queue:
		if not valid_link(source):
			continue
		