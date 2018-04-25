from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import quote
import time
import pymysql.cursors
import os
import argparse
import requests

search_name = input('검색할 제품을 입력하세요 : ') # 네이버에서 검색하여 웹 크롤링 할 제품 이름

'''
# db connect
conn = pymysql.connect(host='localhost',
		user='root',
		password='sorj1256',
		db='jh',
		charset='utf8mb4')
# db 폴더 및 파일 경로
db_path = "C:\\ProgramData\\MySQL\\MySQL Server 5.7\\Data\\jh"
db_name = search_name + '.ibd'
db_save_path = os.path.join(db_path,db_name)

# mysql table 생성 및 테이블 내용 삽입을 위한 명령문
create_table = ' CREATE TABLE ' + search_name + ' ( id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,  goods_url TEXT NOT NULL,  image_src TEXT NOT NULL ) ENGINE=InnoDB DEFAULT CHARSET=utf8 '
insert_into = 'INSERT INTO ' + search_name + '(goods_url, image_src) VALUES (%s, %s)'
load_db = 'SELECT * FROM ' + search_name
db_flags = 0

# 테이블 ,필드 요소 생성 (테이블이 존재하지 않을 경우에만 테이블 생성)
if os.path.isfile(db_save_path) :
	db_flags = 1;
	with conn.cursor() as cursor:
		sql = load_db
		cursor.execute(sql)
		rows = cursor.fetchall()
else :
	with conn.cursor() as cursor:
		sql = create_table
		cursor.execute(sql)
	conn.commit()

i = 0
'''

# 네이버 검색 후 이미지 배너 열기
url_search_name = quote(search_name)
image_search_rul = 'https://search.naver.com/search.naver?where=image&query=' + url_search_name
# image_search_rul = 'https://www.google.co.kr/search?tbm=isch&q=' + url_search_name
req = requests.get(image_search_rul)
html = req.text
soup = BeautifulSoup(html, 'html.parser')

# 검색한 페이지에서 이미지 영역 코드만 가져옴
# photo_grid_box_list = soup.find_all('div','jscontroller')
photo_grid_box_list = soup.select('#_sau_imageTab > div.photowall._photoGridWrapper')
print(photo_grid_box_list)
'''
for img_area in img_area_list:
	goods_str = img_area.findAll('a') # a 태그를 전부 가져옴
	good_url = str(goods_str)[str(goods_str).find('href="')+6:str(goods_str).find('" target=')] # a 태그에 있는 href 를 얻어옴
	utf8_good_url = good_url.encode('utf-8')
	unicode_good_url = utf8_good_url.decode('utf-8')
		
	image_str = img_area.findAll('img') # img 태그를 전부 가져옴
	if str(image_str).find('" height') == -1 :
		image_src = str(image_str)[str(image_str).find('data-original="')+15:str(image_str).find('" src')] # img 태그에 있는 data-original 를 얻어옴
	else:
		image_src = str(image_str)[str(image_str).find('data-original="')+15:str(image_str).find('" height')]
		utf8_image_src = image_src.encode('utf-8')
		unicode_image_src = utf8_image_src.decode('utf-8')
		
		# 이미 db에 존재하는 데이터는 저장하지 않기 위한 조건문(작성중)
		if db_flags == 1 :
			for row in rows :
				print(row[1])
				time.sleep(3)
				if unicode_good_url == row[1] :
					i = i + 1;
					print(i)

		if i == 0 :
			with conn.cursor() as cursor:
				# db 파일에 입력 (제품의 url 주소, 제품의 이미지 src)
				sql = insert_into
				cursor.execute(sql, (unicode_good_url, unicode_image_src))
			conn.commit()
			'''