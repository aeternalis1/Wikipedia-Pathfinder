import json
import requests
from bs4 import BeautifulSoup
from helper import get_page_title


WIKIPEDIA_URL = "https://www.wikipedia.org/w/api.php"


def valid_link(page_id):

	'''
	Arguments:
		[title] - id of page being queried

	Returns:
		[boolean] - True if page is valid, False otherwise
	'''

	params = {
		'action': 'query',
		'format': 'json',
		'pageids': page_id,
		'prop': 'info',
		'redirects': ''
	}

	response = requests.get(WIKIPEDIA_URL, params)

	if response.status_code != 200:
		return False

	data = response.json()['query']['pages']
	print (data)
	for page_id in data:
		if data[page_id]['ns'] or int(page_id) <= 0:		# articles have namespace of 0, everything else doesn't
			return False

	return True


def gen_links(page_id):

	'''
	Arguments:
		[page_id] - id of page being queried

	Returns:
		[links] - '|' separated list of outgoing links from [title] page.
	'''

	params = {
		'action': 'query',
		'pageids': page_id,
		'generator': 'links',
		'format': 'json',
		'gpllimit': 'max',
		'redirects': ''		# ignores redirect page, goes straight to main page
	}

	response = requests.get(WIKIPEDIA_URL, params)

	data = response.json()

	try:
		pages = data['query']['pages']
	except:
		return [], []

	ids = []
	names = []

	for page_id in pages:	
		if pages[page_id]['ns'] or int(page_id) <= 0:
			continue
		ids.append(page_id)
		names.append(pages[page_id]['title'])

	while 'continue' in data:
		for key in data['continue']:
			params[key] = data['continue'][key]
		response = requests.get(WIKIPEDIA_URL, params)

		data = response.json()
		pages = data['query']['pages']

		for page_id in pages:
			if pages[page_id]['ns'] or int(page_id) <= 0:
				continue
			ids.append(page_id)
			names.append(pages[page_id]['title'])

	return ids, names



def get_backlinks(page_id):

	params = {
		'action': 'query',
		'format': 'json',
		'blpageid': page_id,
		'list': 'backlinks',
		'bllimit': 'max'
	}

	response = requests.get(WIKIPEDIA_URL, params)
	data = response.json()
	pages = data['query']['backlinks']

	ids = []
	names = []

	for page in pages:
		if page['ns'] or int(page['pageid']) <= 0:
			continue
		ids.append(page['pageid'])
		names.append(page['title'])

	return ids, names

#print (valid_link('209764'))
#print (valid_link('57700'))

'''
ids, names = gen_links('209764') 

for page_id, page_name in sorted(zip(names, ids)):
	print (page_id, page_name)
'''

'''
ids, names = get_backlinks('21721040')

for page_id, page_name in sorted(zip(names, ids)):
	print (page_id, page_name)
'''


'''
page id of 209764 (Tallahassee) redirects to 57700 (Talahassee, Florida)

BUT this crap counts as an edge. So gotta make a table for redirects so they don't count
as an edge

actually, redirects always only have one 'edge', per se. just stick it in a while loop

'''