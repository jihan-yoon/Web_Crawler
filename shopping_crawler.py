from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import quote
import time
import pymysql.cursors
import os
import argparse
import requests

 # 검색하여 크롤링 할 제품 이름
search_name = input('검색할 제품을 입력하세요 : ')

# db connect
conn = pymysql.connect(host='localhost',
		user='root',
		password='sorj1256',
		db='cloth',
		charset='utf8mb4')

table_name = input('테이블 이름을 입력하세요(English) : ')

# db 폴더 및 파일 경로
idb_directory_path = "C:\\ProgramData\\MySQL\\MySQL Server 5.7\\Data\\jh"
idb_name = table_name + ".ibd"
idb_path = os.path.join(idb_directory_path,idb_name)


# mysql table 생성 및 테이블 내용 삽입을 위한 명령문
create_table = ' CREATE TABLE ' + table_name + ' ( id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, goods_title TEXT NOT NULL, goods_url TEXT NOT NULL,  image_src TEXT NOT NULL ) ENGINE=InnoDB DEFAULT CHARSET=utf8 '
insert_into = ' INSERT INTO ' + table_name + ' (goods_title, goods_url, image_src) VALUES (%s, %s, %s)'
load_db = ' SELECT * FROM ' + table_name

# table 존재 여부 확인을 위한 변수
table_flags = 0 

if os.path.isfile(idb_path):
	table_flags = 1

# 테이블 ,필드 요소 생성 (테이블이 존재하지 않을 경우에만 테이블 생성) -> db 파일 유무 확인 오류
if table_flags == 0 :
	with conn.cursor() as cursor:
		sql = create_table
		cursor.execute(sql)
else :
	with conn.cursor() as cursor:
		sql = load_db
		cursor.execute(sql)
		rows = cursor.fetchall()
		
conn.commit()

print(rows)

# 네이버 쇼핑에서 페이지를 넘겨가면서 크롤링 (num : 네이버 쇼핑에서 제품 검색 후 리스트 페이지 번호)
for num in range(1,2) : 
	url_search_name = quote(search_name)
	shop_search_url = 'https://search.shopping.naver.com/search/all.nhn?pagingIndex=' + str(num) + '&pagingSize=40&query=' + url_search_name
	
	req = requests.get(shop_search_url)
	html = req.text
	soup = BeautifulSoup(html, 'html.parser')
	img_area_list = soup.select('#_search_list > div.search_list.basis > ul > li > div.img_area')

	for img_area in img_area_list:
		a = img_area.find('a') # a 태그를 전부 가져옴
		good_url = a.get('href') # a 태그에 있는 href 를 얻어옴
		utf8_good_url = good_url.encode('utf-8')
		unicode_good_url = utf8_good_url.decode('utf-8')

		img = img_area.find('img') # img 태그를 전부 가져옴
		image_src = img.get('data-original') # img 태그에 있는 data-original 를 얻어옴
		utf8_image_src = image_src.encode('utf-8')
		unicode_image_src = utf8_image_src.decode('utf-8')

		latest_title = img.get('alt')
		
		# 이미 db에 존재하는 데이터는 저장하지 않기 위한 조건문
		if table_flags == 1 :
			for row in rows :
				print(row[1])
				time.sleep(3)
				if unicode_good_url == row[1] :
					i = i + 1;
					print(i)
				else :
					with conn.cursor() as cursor:
						# db 파일에 입력 (제품의 url 주소, 제품의 이미지 src)
						sql = insert_into
						cursor.execute(sql, (latest_title, unicode_good_url, unicode_image_src))
					conn.commit()

		if table_flags == 0 :
			with conn.cursor() as cursor:
				# db 파일에 입력 (제품의 url 주소, 제품의 이미지 src)
				sql = insert_into
				cursor.execute(sql, (latest_title, unicode_good_url, unicode_image_src))
			conn.commit()
			
	num = num + 1