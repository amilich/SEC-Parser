from bs4 import BeautifulSoup
import sys
import urllib
import re
import unicodedata

def parse_amount(amount):
	amount = re.sub(r'[^\(\d]', '', amount)
	amount = amount.replace('(', '-')
	amount = unicodedata.normalize('NFKD', amount).encode('ascii','ignore')
	return amount

def parse_acc_no(acc_no):
	acc = 'Acc-no: '
	acc_index = acc_no.get_text().index(acc)
	acc_length = 20
	
	return acc_no.get_text()[acc_index + len(acc) : acc_index + len(acc) + acc_length].replace('-', '')

def get_acc_no(soup):
	tr = soup.find_all('tr')
	for i in tr:
		report_type = i.find_all('td', nowrap='nowrap')
		for j in report_type:
			if j.get_text() == '10-K':
				return parse_acc_no(i.find('td', class_='small'))

def get_cik_no(soup):
	span = soup.find_all('span', class_='companyName')
	for i in span:
		cik = re.sub(r'\D', '', i.a.get_text())
		for j in range(0, len(cik)):
			if cik[j] != '0':
				return cik[j:]

def get_url(cik):
	url1 = 'https://www.sec.gov/cgi-bin/browse-edgar?CIK='
	url2 = '&owner=exclude&action=getcompany&Find=Search&type=10-k'

	url = url1 + cik + url2
	soup = BeautifulSoup(urllib.urlopen(url).read(), 'lxml')

	cik = get_cik_no(soup)
	acc = get_acc_no(soup)

	url = 'https://www.sec.gov/Archives/edgar/data/' + cik + '/' + acc + '/R'
	for page in range(2, 10):
		statement = url + str(page) + '.htm'
		soup = BeautifulSoup(urllib.urlopen(statement).read(), 'lxml')

		# print statement		
		title = soup.find('th', class_='tl').get_text().lower()
		if ('consolidated balance sheet'in title or 'consolidated statement of financial position' in title) and not 'parenthetical' in title:
			return statement, 10**3 if 'thousand' in title else 10**6 if 'million' in title else 10**9

def parse(ticker):
	url = get_url(ticker)
	soup = BeautifulSoup(urllib.urlopen(url[0]).read(), 'lxml')

	all_entries = soup.find_all('tr', {'class':['re', 'ro', 'reu', 'rou', 'rh']})
	for entry in all_entries:
		title = entry.find('a', class_='a').get('onclick')
		numbers = entry.find_all('td', {'class':['nump', 'num']})

		if 'us-gaap_AssetsCurrent\'' in title:
			for amount in numbers:
				yield float(parse_amount(amount.get_text())) * url[1]
				break
		elif 'us-gaap_LiabilitiesCurrent\'' in title:
			for amount in numbers:
				yield float(parse_amount(amount.get_text())) * url[1]
				break
		elif 'us-gaap_PropertyPlantAndEquipmentNet\'' in title:
			for amount in numbers:
				yield float(parse_amount(amount.get_text())) * url[1]
				break