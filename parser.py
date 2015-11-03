from bs4 import BeautifulSoup
import sys
import urllib
import re
import unicodedata

def parse_acc_no(acc_no):
	acc = 'Acc-no: '
	acc_index = acc_no.get_text().index(acc)
	acc_length = 20
	
	return acc_no.get_text()[acc_index + len(acc) : acc_index + len(acc) + acc_length].replace('-', '')

def get_acc_no(soup):
	tr = soup.find_all('tr')
	for i in tr:
		found = False
		td_nowrap = i.find_all('td', nowrap='nowrap')
		for j in td_nowrap:
			if j.get_text() == '10-Q':
				found = True
				break

		td_class = i.find_all('td', class_='small')
		for j in td_class:
			return parse_acc_no(j)

		if found:
			break

def get_cik_no(soup):
	span = soup.find_all('span', class_='companyName')
	for i in span:
		cik = re.sub(r'\D', '', i.a.get_text())
		for j in range(0, len(cik)):
			if cik[j] != '0':
				return cik[j:]

def get_url(cik):
	url1 = 'https://www.sec.gov/cgi-bin/browse-edgar?CIK='
	url2 = '&owner=exclude&action=getcompany&Find=Search'

	url = url1 + cik + url2
	soup = BeautifulSoup(urllib.urlopen(url).read(), 'lxml')

	cik = get_cik_no(soup)
	acc = get_acc_no(soup)
	return 'https://www.sec.gov/Archives/edgar/data/' + cik + '/' + acc + '/R2.htm'

def parse(soup):
	lines = soup.find_all('tr', {'class':['re', 'ro', 'reu', 'rou', 'rh']})
	sec_table = {}
	for i in lines:
		pl = i.find_all('a', class_='a')
		num = i.find_all('td', {'class':['nump', 'num']})

		amount = []
		for j in num:
			text = re.sub(r'[\s$,]', '', j.get_text())
			if '(' or ')' in text:
				text = text.replace(')', '').replace('(', '-')
			text = unicodedata.normalize('NFKD', text).encode('ascii','ignore')
			amount.append(int(text))

		if len(num) > 0:
			print pl[0].get_text()
			print amount
			sec_table[pl[0].get_text()] = amount

def main():
	ticker = raw_input('Enter ticker symbol: ').lower()
	soup = BeautifulSoup(urllib.urlopen(get_url(ticker)).read(), 'lxml')
	parse(soup)

main()