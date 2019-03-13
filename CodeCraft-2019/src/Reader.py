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
from Car import Car
from Cross import Cross
from Road import Road

class Reader(object):

	def __init__(self, data_dir):
		"""
		to get the list of cars, crosses and road
		:param data_dir:
		"""
		self.__car_file = os.path.join(data_dir, 'car.txt')
		self.__cross_file = os.path.join(data_dir, 'cross.txt')
		self.__road_file = os.path.join(data_dir, 'road.txt')

	def get_cars(self):
		with open(self.__car_file, 'r') as file_car:
			content = file_car.read()
			pattern = r'.*?([0-9]+).*?([0-9]+).*?([0-9]+).*?([0-9]+).*?([0-9]+).*?'
			data_list = re.findall(pattern, content)
			car_list = list()
			for obj in data_list:
				car_list.append(Car(obj[0], obj[1], obj[2], obj[3], obj[4]))
			return car_list

	def get_crosses(self):
		with open(self.__cross_file, 'r') as file_cross:
			content = file_cross.read()
			pattern = r'.*?([0-9]+).*?([0-9]+).*?([0-9]+).*?([0-9]+).*?([0-9]+).*?'
			data_list = re.findall(pattern, content)
			cross_list = list()
			for obj in data_list:
				cross_list.append(Cross(obj[0], obj[1], obj[2], obj[3], obj[4]))
			return cross_list

	def get_roads(self):
		with open(self.__road_file, 'r') as file_road:
			content = file_road.read()
			pattern = r'.*?([0-9]+).*?([0-9]+).*?([0-9]+)' \
			          r'.*?([0-9]+).*?([0-9]+).*?([0-9]+).*?([0-9]+).*?'
			data_list = re.findall(pattern, content)
			road_list = list()
			for obj in data_list:
				road_list.append(Road(obj[0], obj[1], obj[2], obj[3], obj[4], obj[5], obj[6]))
			return road_list

if __name__ == '__main__':
	reader = Reader('../config')
	for car in reader.get_cars():
		print(car)