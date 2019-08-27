import json
import requests
from bs4 import BeautifulSoup


WIKIPEDIA_URL = "https://www.wikipedia.org/w/api.php"


def valid_link(title):

	params = {
		'action': 'query',
		'format': 'json',
		'titles': title,
		'prop': 'info',
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


def get_links(title): 			# returns list of [cur_page_id, next_page_title]

	params = {
		'action': 'query',
		'format': 'json',
		'titles': title,
		'prop': 'links',
		'pllimit': 'max'
	}

	response = requests.get(WIKIPEDIA_URL, params)

	data = response.json()
	pages = data['query']['pages']

	links = []

	for page_id in pages:
		if 'links' not in pages[page_id]:
			continue
		for link in pages[page_id]['links']:
			if link['ns'] == 0:			# articles have namespace of 0
				links.append([page_id, link['title']])	

	while 'continue' in data:
		for key in data['continue']:
			params[key] = data['continue'][key]
		response = requests.get(WIKIPEDIA_URL, params)

		data = response.json()
		pages = data['query']['pages']

		for page_id in pages:
			if 'links' not in pages[page_id]:
				continue
			for link in pages[page_id]['links']:
				if link['ns'] == 0:			# articles have namespace of 0
					links.append([page_id, link['title']])	

	return links



def gen_links(page):

	params = {
		'action': 'query',
		'pageids': page,
		'generator': 'links',
		'format': 'json',
		'gpllimit': 'max'
	}

	response = requests.get(WIKIPEDIA_URL, params)
	data = response.json()
	try:
		pages = data['query']['pages']
	except:
		print (data, page) 
	ids = []
	names = []

	for page_id in pages:	
		if pages[page_id]['ns'] or int(page_id) <= 0:
			continue
		ids.append(page_id)
		names.append(pages[page_id]['title'])

	return ids, names



def get_backlinks(title):

	params = {
		'action': 'query',
		'format': 'json',
		'bltitle': title,
		'list': 'backlinks',
		'bllimit': 'max'
	}

	response = requests.get(WIKIPEDIA_URL, params)

	data = response.json()

	pages = data['query']['backlinks']

	return [item['title'] for item in pages]


#print (len(gen_links('King Duncan|Jimmie')))
#print (len(get_links('King Duncan|Macbeth|Mathematics')))
#print (valid_link('Adalbert_Matkowsky'))
#print (get_page_title('18630637'))