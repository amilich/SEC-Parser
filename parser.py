from bs4 import BeautifulSoup
import urllib
import re
import unicodedata

name = 'https://www.sec.gov/Archives/edgar/data/1288776/000128877615000046/R5.htm'
url = urllib.urlopen(name).read()
soup = BeautifulSoup(url, 'lxml')
# print type(soup)
# print soup.prettify()

lines = soup.find_all('tr', {'class':['re', 'ro', 'reu', 'rou', 'rh']})

sec_table = {}
for i in lines:
	pl = i.find_all('a', class_='a')
	num = i.find_all('td', {'class':['nump', 'num']})

	amount = []
	for j in num:
		text = re.sub(r"[\s$,]", "", j.get_text())
		if '(' or ')' in text:
			text = text.replace(')', "").replace('(', '-')
		text = unicodedata.normalize('NFKD', text).encode('ascii','ignore')
		amount.append(int(text))

	if len(num) > 0:
		print pl[0].get_text()
		print amount
		sec_table[pl[0].get_text()] = amount

# print sec_table