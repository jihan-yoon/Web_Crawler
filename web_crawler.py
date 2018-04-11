from bs4 import BeautifulSoup
from urllib.request import urlopen
import pymysql.cursors
import os
import argparse

f = open('images_src.txt','w')

ap = argparse.ArgumentParser()
ap.add_argument("-sl", "--search_list", required=True,
	help="path to file containing search_list")
args = vars(ap.parse_args())
rows = open(args["urls"]).read().strip().split("\n")

# db connect
conn = pymysql.connect(host='localhost',
		user='root',
		password='sorj1256',
		db='jh',
		charset='utf8mb4')

# 테이블 ,필드 요소 생성 (테이블이 이미 존재할경우 테이블 생성 x)
if os.path.exists("C:\ProgramData\MySQL\MySQL Server 5.7\Data\jh\mtm_data.ibd"):
	with conn.cursor() as cursor:
		sql = '''
			DROP TABLE mtm_data
		'''
		cursor.execute(sql)
	conn.commit()

with conn.cursor() as cursor:
	sql = '''
	CREATE TABLE mtm_data (
	id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
	goods_url TEXT NOT NULL,
	image_src TEXT NOT NULL
	) ENGINE=InnoDB DEFAULT CHARSET=utf8
	'''
	cursor.execute(sql)
conn.commit()

for num in range(1,100) : # num : 네이버 쇼핑에서 제품 검색 후 페이지 번호
	s = str(num) 
	search_name = '맨투맨'
	
	url_search_name = quote(search_name)
	str1 = 'https://search.shopping.naver.com/search/all.nhn?origQuery=' + url_search_name + '&pagingIndex='
	str2 = '&pagingSize=80&viewType=list&sort=rel&frm=NVSHPAG&query=' + url_search_name # pagingSize : 한 페이지 제품 개수
	useurl = str1 + s + str2
	
	html = urlopen(useurl)
	soup = BeautifulSoup(html,"lxml")
	eee = soup.find_all('img')
	uuu = soup.find_all('div','img_area')
	
	for u in uuu:
		goods_str = u.findAll('a')
		good_url = str(goods_str)[str(goods_str).find('href="')+6:str(goods_str).find('" target=')]
		utf8_good_url = good_url.encode('utf-8')
		unicode_good_url = utf8_good_url.decode('utf-8')
		
		image_str = u.findAll('img')
		if str(image_str).find('" height') == -1 :
			image_src = str(image_str)[str(image_str).find('data-original="')+15:str(image_str).find('" src')]
		else:
			image_src = str(image_str)[str(image_str).find('data-original="')+15:str(image_str).find('" height')]
		utf8_image_src = image_src.encode('utf-8')
		unicode_image_src = utf8_image_src.decode('utf-8')
		
		# 제품 이미지 다운로드를 위해 이미지 src 를 텍스트 파일로 출력
		f.write(unicode_image_src)
		f.write('\n')
			
		with conn.cursor() as cursor:
			sql = 'INSERT INTO mtm_data (goods_url, image_src) VALUES (%s, %s)'
			# db 파일에 입력 (제품의 url 주소, 제품의 이미지 src)
			cursor.execute(sql, (unicode_good_url, unicode_image_src))
				
		conn.commit()
			
		
	num = num + 1;

f.close