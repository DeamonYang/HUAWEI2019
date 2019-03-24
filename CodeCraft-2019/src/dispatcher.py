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

class Dispatcher(object):

	def __init__(self, car_list, road_list, cross_list):

		self.__car_list = car_list
		self.__road_list = road_list
		self.__cross_list = cross_list

		self.__crossId_to_sorted_cars = {}  # 起点对应的按车速和安排排好序的车辆列表
		for cross in self.__cross_list:
			self.__crossId_to_sorted_cars[cross.cross_id] = []
		self.__sort_cars()

		self.__gragh = Graph(self.__road_list, self.__cross_list)

		self.__crossIds_to_road = {}
		for road in self.__road_list:
			crossIds = road.road_from + '_' + road.road_to
			self.__crossIds_to_road[crossIds] = road
			if road.road_isDuplex == '1':
				crossIds = road.road_to + '_' + road.road_from
				self.__crossIds_to_road[crossIds] = road

		self.__car_number_each_time = 17


	def run(self):
		schedule_list = list()

		i = 0   # schedule_counter
		while i < len(self.__car_list) // self.__car_number_each_time:
			if i + 1 == len(self.__car_list) // self.__car_number_each_time:
				running_cars = self.__car_list[self.__car_number_each_time * i : ]
			else:
				running_cars = self.__car_list[self.__car_number_each_time * i : self.__car_number_each_time * (i + 1)]
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

		key_list = list(self.__carSpeed_to_cars.keys())
		key_list.sort(reverse=True) # 按安排的时间进行升序排序
		for key in key_list:
			self.__carSpeed_to_cars[key].sort(key=Car.get_planTime, reverse=False)  # 按速度排序
			for car in self.__carSpeed_to_cars[key]:
				self.__crossId_to_sorted_cars[car.car_from].append(car)
		sorted_cars_matrix = list(self.__crossId_to_sorted_cars.values())

		car_number = len(self.__car_list)
		car_counter  = 0
		j = 0                                           # j is col index of 'sorted_cars_matrix'
		while car_counter < car_number:
			for i in range(len(sorted_cars_matrix)):    # i is row index of 'sorted_cars_matrix'
				if j < len(sorted_cars_matrix[i]):
					car_list_sorted.append(sorted_cars_matrix[i][j])
					car_counter += 1
			j += 1
		self.__car_list = car_list_sorted
		# for car in self.__car_list:
		# 	print(car)
		# print(len(self.__cross_list)) 64


