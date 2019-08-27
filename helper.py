import json
import requests
from bs4 import BeautifulSoup


WIKIPEDIA_URL = "https://www.wikipedia.org/w/api.php"


def get_page_id(title):		# returns page_id as a string, with page_name as argument
	params = {
		'action': 'query',
		'format': 'json',
		'titles': title,
		'prop': 'info',
		'pllimit': 'max'
	}

	response = requests.get(WIKIPEDIA_URL, params)

	data = response.json()['query']['pages']

	for page_id in data:
		return page_id


def get_page_title(page_id):
	params = {
		'action': 'query',
		'format': 'json',
		'pageids': page_id,
		'prop': 'info',
		'pllimit': 'max'
	}

	response = requests.get(WIKIPEDIA_URL, params)

	data = response.json()['query']['pages']

	for page_id in data:
		return data[page_id]['title']