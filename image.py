from bs4 import BeautifulSoup
from urllib.request import urlopen

f = open('urls.txt','w')

html = urlopen('https://search.shopping.naver.com/search/all.nhn?query=%EB%82%A8%EC%9E%90+%EB%A7%A8%ED%88%AC%EB%A7%A8&cat_id=&frm=NVSHATC')
soup = BeautifulSoup(html,"lxml")
eee = soup.find_all("img")

for m in eee:
	f.write(m.get('src'))
	f.write("\n")

f.close