from bs4 import BeautifulSoup
import urllib

name = "https://www.sec.gov/Archives/edgar/data/320193/000119312515259935/R3.htm"
url = urllib.urlopen(name).read()
soup = BeautifulSoup(url, 'lxml')
print type(soup)
# print soup.prettify()

lines = soup.find_all("tr", {"class":["re", "ro", "reu", "rou", "rh"]})

for i in lines:
	pl = i.find_all("td", class_="pl ")
	for j in pl:
		print j.get_text()

	num = i.find_all("td", {"class":["pl ", "nump", "num"]})
	for j in num:
		print j.get_text()