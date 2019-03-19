'''
--------------------------------------------------------
@File    :   dispatcher.py    
@Contact :   1183862787@qq.com
@License :   (C)Copyright 2017-2018, CS, WHU

@Modify Time : 2019/3/15 11:23     
@Author      : Liu Wang    
@Version     : 1.0   
@Desciption  : None
--------------------------------------------------------  
'''
from graph import Graph
from pojo import Schedule
from pojo import Car
import random

class Dispatcher(object):

	def __init__(self, car_list, road_list, cross_list):

		self.__car_list = car_list
		self.__road_list = road_list
		self.__cross_list = cross_list

		self.__sort_cars()

		self.__gragh = Graph(self.__road_list, self.__cross_list)

		self.__crossIds_to_road = {}
		for road in self.__road_list:
			crossIds = road.road_from + '_' + road.road_to
			self.__crossIds_to_road[crossIds] = road
			if road.road_isDuplex == '1':
				crossIds = road.road_to + '_' + road.road_from
				self.__crossIds_to_road[crossIds] = road

	def run(self):
		schedule_list = list()
		car_number_each_time = 15

		i = 0   # schedule_counter
		while i < len(self.__car_list) // car_number_each_time:
			if i + 1 == len(self.__car_list) // car_number_each_time:
				running_cars = self.__car_list[car_number_each_time * i : ]
			else:
				running_cars = self.__car_list[car_number_each_time * i : car_number_each_time * (i + 1)]
			for car in running_cars:
				cross_id_from = car.car_from
				cross_id_to = car.car_to
				cross_list = self.__gragh.get_min_trace(cross_id_from, cross_id_to)
				road_list = list()
				for index in range(len(cross_list) - 1):
					crossIds = cross_list[index].cross_id + '_' + cross_list[index+1].cross_id
					road_list.append(self.__crossIds_to_road[crossIds])
				schedule = Schedule(car, i + car.car_planTime, road_list)
				schedule_list.append(schedule)
			i += 1
		return schedule_list

	def __sort_cars(self):
		car_list_sorted = []
		# 按速度将车归类
		self.__carSpeed_to_cars = {}
		for car in self.__car_list:
			if str(car.car_speed) in self.__carSpeed_to_cars.keys():
				self.__carSpeed_to_cars[str(car.car_speed)].append(car)
			else:
				self.__carSpeed_to_cars[str(car.car_speed)] = [car]
		# 按安排的时间进行升序排序
		key_list = list(self.__carSpeed_to_cars.keys())
		key_list.sort(reverse=True)
		for key in key_list:
			random.shuffle(self.__carSpeed_to_cars[key])
			self.__carSpeed_to_cars[key].sort(key=Car.get_planTime, reverse=False)
			for car in self.__carSpeed_to_cars[key]:
				car_list_sorted.append(car)
				# print(car)
		self.__car_list = car_list_sorted


