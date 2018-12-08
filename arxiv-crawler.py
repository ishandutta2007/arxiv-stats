import os, sys, unittest, time, re, requests
from bs4 import BeautifulSoup
import traceback

import urllib.error
from urllib.request import Request, urlopen, build_opener, install_opener, HTTPBasicAuthHandler, HTTPPasswordMgrWithDefaultRealm
from lxml import etree
import time
from datetime import date, datetime
from requests import session

def get_page(year, month):
	try:
		if not os.path.exists('data/arxiv/' + format(year%100, '02') + format(month, '02') + '.csv'):
			req = Request("https://arxiv.org/list/stat/" + format(year%100, '02') + format(month, '02') + "?show=2000", headers={'User-Agent': 'Mozilla/5.0'})
			html_source = urlopen(req).read()
			parsed_html = BeautifulSoup(html_source, 'html.parser')
			links = parsed_html.find_all("a", { 'title' :'Abstract' })
			titles = parsed_html.find_all("div",class_="list-title mathjax")
			if len(links) > 0:
				with open('data/arxiv/' + format(year%100, '02') + format(month, '02') + '.csv','w') as file:
					for i in range(len(links)):
						file.write(links[i].text.strip() + ', ' + titles[i].text.strip() + '\n')
						print(links[i].text.strip(), titles[i].text.strip())
	except Exception:
		traceback.print_exc()

def main():
	d = os.listdir('data/arxiv')
	d.sort()
	os.unlink('data/arxiv/'+d[-1])
	for year in range(2007, datetime.now().year+1):
		for month in range(1, 13):
			get_page(year, month)

if __name__ == '__main__':
  main()