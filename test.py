from bs4 import BeautifulSoup
import urllib

def parse_acc_no(acc_no):
	acc = 'Acc-no: '
	acc_index = acc_no.get_text().index(acc)
	acc_length = 20
	
	return acc_no.get_text()[acc_index + len(acc) : acc_index + len(acc) + acc_length].replace('-', '')

def get_acc_no():
	url1 = 'https://www.sec.gov/cgi-bin/browse-edgar?CIK='
	cik = 'googl'
	url2 = '&owner=exclude&action=getcompany&Find=Search'

	url = url1 + cik + url2
	soup = BeautifulSoup(urllib.urlopen(url).read(), 'lxml')

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

print get_acc_no()