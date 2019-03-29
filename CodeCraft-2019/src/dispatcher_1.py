'''
--------------------------------------------------------
@File    :   dispatcher_1.py
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

		self.__gragh = Graph(self.__road_list, self.__cross_list)

		self.__sort_cars()

		self.__crossIds_to_road = {}
		for road in self.__road_list:
			crossIds = road.road_from + '_' + road.road_to
			self.__crossIds_to_road[crossIds] = road
			if road.road_isDuplex == '1':
				crossIds = road.road_to + '_' + road.road_from
				self.__crossIds_to_road[crossIds] = road

		self.__car_number_each_clock = 15


	def run(self):
		schedule_list = []
		index = 0
		clock = 0
		while (index+1)*self.__car_number_each_clock < len(self.__car_list):
			car_list = self.__car_list[index*self.__car_number_each_clock:(1+index)*self.__car_number_each_clock]
			for car in car_list:
				cross_id_from = car.car_from
				cross_id_to = car.car_to
				cross_list = self.__gragh.get_min_trace(cross_id_from, cross_id_to)
				road_list = list()
				for j in range(len(cross_list) - 1):
					crossIds = cross_list[j].cross_id + '_' + cross_list[j + 1].cross_id
					road_list.append(self.__crossIds_to_road[crossIds])
				schedule = Schedule(car, clock + car.car_planTime, road_list)
				schedule_list.append(schedule)
			index += 1
			clock += 1

		car_list = self.__car_list[index * self.__car_number_each_clock:]
		for car in car_list:
			cross_id_from = car.car_from
			cross_id_to = car.car_to
			cross_list = self.__gragh.get_min_trace(cross_id_from, cross_id_to)
			road_list = list()
			for j in range(len(cross_list) - 1):
				crossIds = cross_list[j].cross_id + '_' + cross_list[j + 1].cross_id
				road_list.append(self.__crossIds_to_road[crossIds])
			schedule = Schedule(car, clock + car.car_planTime, road_list)
			schedule_list.append(schedule)
		return schedule_list


	def __sort_cars(self):

		result = []
		speed_to_cars_dict = {}
		for car in self.__car_list:
			if str(car.car_speed) not in speed_to_cars_dict.keys():
				speed_to_cars_dict[str(car.car_speed)] = []
			speed_to_cars_dict[str(car.car_speed)].append(car)
		keys = list(speed_to_cars_dict.keys())
		keys_int = [int(e) for e in keys]
		keys_int.sort(reverse=True)
		for key_int in keys_int:
			car_list = speed_to_cars_dict[str(key_int)]
			car_list.sort(key=Car.get_Id)
			result.extend(car_list)
		self.__car_list = result

		# print("sort finished")







