'''
--------------------------------------------------------
@File    :   reader.py.py    
@Contact :   1183862787@qq.com
@License :   (C)Copyright 2017-2018, CS, WHU

@Modify Time : 2019/3/13 21:50     
@Author      : Liu Wang    
@Version     : 1.0   
@Desciption  : None
--------------------------------------------------------  
''' 

import os
import re
from pojo import *

class Reader(object):

	def __init__(self, car_file, cross_file, road_file):
		"""
		to get the list of cars, crosses and road
		:param data_dir:
		"""
		self.__car_file = os.path.join('./', car_file)
		self.__cross_file = os.path.join('./', cross_file)
		self.__road_file = os.path.join('./', road_file)

	def get_cars(self):
		with open(self.__car_file, 'r', encoding='utf-8') as file_car:
			content = file_car.read()
			pattern = r'.*?([0-9]+).*?([0-9]+).*?([0-9]+).*?([0-9]+).*?([0-9]+).*?'
			data_list = re.findall(pattern, content)
			car_list = list()
			for obj in data_list:
				car_list.append(Car(obj[0], obj[1], obj[2], int(obj[3]), int(obj[4])))
			return car_list

	def get_crosses(self):
		with open(self.__cross_file, 'r', encoding='utf-8') as file_cross:
			content = file_cross.read()
			pattern = r'.*?([0-9]+).*?([0-9\-]+).*?([0-9\-]+).*?([0-9\-]+).*?([0-9\-]+).*?'
			data_list = re.findall(pattern, content)
			cross_list = list()
			for obj in data_list:
				cross_list.append(Cross(obj[0], obj[1], obj[2], obj[3], obj[4]))
			return cross_list

	def get_roads(self):
		with open(self.__road_file, 'r', encoding='utf-8') as file_road:
			content = file_road.read()
			pattern = r'.*?([0-9]+).*?([0-9]+).*?([0-9]+)' \
			          r'.*?([0-9]+).*?([0-9]+).*?([0-9]+).*?([0-9]+).*?'
			data_list = re.findall(pattern, content)
			road_list = list()
			for obj in data_list:
				road_list.append(Road(obj[0], int(obj[1]), int(obj[2]), int(obj[3]), obj[4], obj[5], obj[6]))
			return road_list



if __name__ == '__main__':
	reader = Reader('../config/car.txt', '../config/cross.txt', '../config/road.txt', )
	for obj in reader.get_roads():
		print(obj)