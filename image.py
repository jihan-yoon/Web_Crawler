from bs4 import BeautifulSoup
from urllib.request import urlopen
# import sqlite3
import pymysql.cursors
import MySQLdb

f = open('images_src.txt','w')

import pymysql.cursors

conn = pymysql.connect(host='localhost',
		user='root',
		password='sorj1256',
		db='jh',
		charset='utf8mb4')	


with conn.cursor() as cursor:
	sql = '''
	CREATE TABLE mtm_data (
	id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
	goods_url varchar(255) NOT NULL,
	image_src varchar(255) NOT NULL
	) ENGINE=InnoDB DEFAULT CHARSET=utf8
	'''
	cursor.execute(sql)
conn.commit()

for num in range(1,100) :
	s = str(num)
	str1 = 'https://search.shopping.naver.com/search/all.nhn?origQuery=%EB%A7%A8%ED%88%AC%EB%A7%A8&pagingIndex='
	str2 = '&pagingSize=80&viewType=list&sort=rel&frm=NVSHPAG&query=%EB%A7%A8%ED%88%AC%EB%A7%A8' # pagingSize : 한 페이지 제품 개수
	useurl = str1 + s + str2
	html = urlopen(useurl)
	soup = BeautifulSoup(html,"lxml")
	eee = soup.find_all('img')
	uuu = soup.find_all('a')
	
	for u in uuu:
		for m in eee:
			i = 1;
			f.write(str(m.get('data-original')))
			f.write('\n')
			
			with conn.cursor() as cursor:
				sql = 'INSERT INTO mtm_data (goods_url, image_src) VALUES (%s, %s)'
				cursor.execute(sql, (str(u.get('href')), str(m.get('data-original'))))
				
			conn.commit()
			
			i = i + 1;
		
	num = num + 1;

f.close