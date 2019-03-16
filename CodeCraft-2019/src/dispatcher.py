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


class Dispatcher(object):

	def __init__(self, car_list, road_list, cross_list):

		self.__car_list = car_list
		self.__road_list = road_list
		self.__cross_list = cross_list
		# for crs in self.__cross_list:
		# 	print(crs)
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
		counter = 0
		for car in self.__car_list:
			cross_id_from = car.car_from
			cross_id_to = car.car_to
			cross_list = self.__gragh.get_min_trace(cross_id_from, cross_id_to)
			road_list = list()
			for index in range(len(cross_list) - 1):
				crossIds = cross_list[index].cross_id + '_' + cross_list[index+1].cross_id
				road_list.append(self.__crossIds_to_road[crossIds])
			schedule = Schedule(car, car.car_planTime + counter / 5, road_list)
			schedule_list.append(schedule)
			counter += 1
		return schedule_list
