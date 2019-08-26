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

	for page_id in data:
		if data[page_id]['ns']:		# articles have namespace of 0, everything else doesn't
			return False

	return True


def get_links(title):

	params = {
		'action': 'query',
		'format': 'json',
		'titles': title,
		'prop': 'links',
		'pllimit': 'max'
	}

	response = requests.get(WIKIPEDIA_URL, params)

	data = response.json()

	pages = data['query']['pages']['links']

	links = []

	for k, v in pages.items():
		for link in v['links']:
			if link['ns'] == 0:			# articles have namespace of 0
				links.append(link['title'])

	return links


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


print (get_links('King Duncan'))