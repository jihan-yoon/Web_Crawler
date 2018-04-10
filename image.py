from bs4 import BeautifulSoup
from urllib.request import urlopen

f = open('images_src.txt','w')

for num in range(1,100) :
	s = str(num)
	str1 = 'https://search.shopping.naver.com/search/all.nhn?origQuery=%EB%A7%A8%ED%88%AC%EB%A7%A8&pagingIndex='
	str2 = '&pagingSize=80&viewType=list&sort=rel&frm=NVSHPAG&query=%EB%A7%A8%ED%88%AC%EB%A7%A8' # pagingSize : 한 페이지 제품 개수
	useurl = str1 + s + str2
	html = urlopen(useurl)
	soup = BeautifulSoup(html,"lxml")
	eee = soup.find_all('img')
	uuu = soup.find_all('a')
	
	print(uuu)

	for m in eee:
		f.write(str(m.get('data-original')))
		f.write('\n')
	num = num + 1;

f.close