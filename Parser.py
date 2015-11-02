from bs4 import BeautifulSoup
import urllib
import unicodedata

name = "https://www.sec.gov/Archives/edgar/data/320193/000119312515259935/R3.htm"
url = urllib.urlopen(name).read()
soup = BeautifulSoup(url, 'lxml')
# print type(soup)
# print soup.prettify()

lines = soup.find_all("tr", {"class":["re", "ro", "reu", "rou", "rh"]})

sec_table = {}
for i in lines:
	pl = i.find_all("td", class_="pl ")
	num = i.find_all("td", {"class":["nump", "num"]})

	amount = []
	for j in num:
		# print j.get_text()
		text = unicodedata.normalize('NFKD', j.get_text()[:-1]).encode('ascii','ignore')
		amount.append(text)

	if len(num) > 0:
		print pl[0].get_text()
		print amount
		sec_table[pl[0].get_text()] = amount

# print sec_table