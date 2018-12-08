import os, sys, unittest, time, re, requests
from bs4 import BeautifulSoup
import traceback

import json
import hashlib
import urllib.error
from urllib.request import Request, urlopen, build_opener, install_opener, HTTPBasicAuthHandler, HTTPPasswordMgrWithDefaultRealm
from lxml import etree
import csv
import time
import logging
from datetime import date, datetime
import subprocess
from requests import session

from google import google
import re

username_pattern = '[a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38}'
reponame_pattern = '([a-z\d]|[A-Z\d])(?:[a-z\d]|[A-Z\d]|-(?=[a-z\d]|[A-Z\d])){0,200}'
repourl_pattern = '^https://github.com/' + username_pattern + '/' + reponame_pattern + '$'

def purify(search_term):
	search_term = search_term.replace('math/', '')
	search_term = search_term.replace('physics/', '')
	search_term = search_term.replace('q-bio/', '')
	return search_term

def search_texts(attribute):
	try:
		time.sleep(10)
		arxiv_id = attribute[0].replace('arXiv:','').strip()
		title = attribute[1].replace('Title:','').strip()
		search_term = "github:\"" + arxiv_id + "\""
		search_term = purify(search_term)
		print(search_term)
		search_results = google.search(search_term, 1)
		found = False
		for index, gResult in enumerate(search_results):
			if re.search(repourl_pattern, gResult.link):
				found = True
				print(search_term, index, " ====> ", gResult.link)
				break
		if found==False:
			print(search_term, " ====> ", "NOT FOUND")

	except Exception:
		traceback.print_exc()

if __name__ == '__main__':
	files = os.listdir('data/arxiv')
	files.sort(reverse=True)
	for file in files:
		with open('data/arxiv/' + file,'r') as file:
			msg_reader = csv.reader(file)
			next(msg_reader)
			list(map(lambda x: search_texts(x), msg_reader))
