import time
import os
from PIL import Image

# bbox 좌표 텍스트 파일 경로
txt_path = "D:\\mnasdfa\\Category and Attribute Prediction Benchmark\\Anno\\list_bbox.txt"
f = open(txt_path, 'r')
lines = f.readlines()
f.close()

# 학습에 사용하는 이미지 경로가 적힌 텍스트 파일
img_path_txt = "D:\\mnasdfa\\darknet\\yolo-for-windows-v2\\build\\darknet\\x64\\data\\train.txt"
c = open(img_path_txt,'w')
i = 1

for line in lines :
	if i >= 3 :
		train_img_path_txt = str(line)[0:str(line).find('.jpg')+4]
		c.write(train_img_path_txt)
		c.write('\n')
	i = i + 1

c.close()
'''
i = 1
j = 1

# 이미지 타입을 받아오기 위한 텍스트 파일
img_type_txt = "D:\\mnasdfa\\Category and Attribute Prediction Benchmark\\Anno\\list_category_img.txt"
f = open(img_type_txt, 'r')
lines2 = f.readlines()
f.close()

for line2 in lines2 :
	if i >= 3 :
		# 이미지와 같은 경로에 box 좌표 텍스트 파일 경로
		img_txt = str(line2)[0:str(line2).find('.jpg')]
		img_txt_replaceAll= img_txt.replace("/","\\")
		img_txt_name = img_txt_replaceAll + ".txt"
		img_txt_path = os.path.join("D:\\mnasdfa\\darknet\\yolo-for-windows-v2\\build\darknet\\x64\\img",img_txt_name)

		# 이미지 타입 및 좌표 입력을 위한 텍스트 파일 열기
		f = open(img_txt_path,'w')

		# 이미지 타입 입력
		img_type = line2[71]
		data1 = str(img_type) + " "
		f.write(data1)
	i = i + 1
f.close()

for line in lines :
	if j>=3 :
		# 이미지 경로 및 이미지 로드
		img_path_txt = str(line)[0:str(line).find('.jpg')+4]
		img_path_txt_replaceAll= img_path_txt.replace("/","\\")
		img_path = os.path.join("D:\\mnasdfa\\darknet\\yolo-for-windows-v2\\build\darknet\\x64\\img",img_path_txt_replaceAll)

		# 이미지 로드 및 이미지 사이즈 반한
		i = Image.open(img_path)
		img_width , img_height = i.size

		img_txt = str(line)[0:str(line).find('.jpg')]
		img_txt_replaceAll= img_txt.replace("/","\\")
		img_txt_name = img_txt_replaceAll + ".txt"
		img_txt_path = os.path.join("D:\\mnasdfa\\darknet\\yolo-for-windows-v2\\build\darknet\\x64\\img",img_txt_name)
		f = open(img_txt_path,'a')

		x1 = int(line[71:74])
		y1 = int(line[75:78])
		x2 = int(line[79:82])
		y2 = int(line[83:86])				

		# box 사이즈 및 center x,y 좌표
		width = x2-x1
		height = y2-y1
		cx = (x1+x2)/2
		cy = (y1+y2)/2

		data2 =  str(cx/img_width) + " " + str(cy/img_height) + " " + str(width/img_width) + " " + str(height/img_height)
		f.write(data2)
	j = j + 1 

f.close()
'''