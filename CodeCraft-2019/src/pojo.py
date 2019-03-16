'''
--------------------------------------------------------
@File    :   pojo.py    
@Contact :   1183862787@qq.com
@License :   (C)Copyright 2017-2018, CS, WHU

@Modify Time : 2019/3/14 16:04     
@Author      : Liu Wang    
@Version     : 1.0   
@Desciption  : None
--------------------------------------------------------  
''' 

class Car(object):

	def __init__(self, car_id,
	             car_from,
	             car_to,
	             car_speed,
	             car_planTime):
		self.car_id = car_id
		self.car_from = car_from
		self.car_to = car_to
		self.car_speed = car_speed
		self.car_planTime = car_planTime

	def __str__(self):
		return str('(' + self.car_id + ','
		           + self.car_from + ','
		           + self.car_to + ','
		           + str(self.car_speed) + ','
		           + str(self.car_planTime) + ')')



class Cross(object):

	def __init__(self, cross_id,
	             cross_road_id_1,
	             cross_road_id_2,
	             cross_road_id_3,
	             cross_road_id_4):
		self.cross_id = cross_id
		self.cross_road_id_1 = cross_road_id_1
		self.cross_road_id_2 = cross_road_id_2
		self.cross_road_id_3 = cross_road_id_3
		self.cross_road_id_4 = cross_road_id_4

	def __str__(self):
		return str('(' + self.cross_id + ','
		           + self.cross_road_id_1 + ','
		           + self.cross_road_id_2 + ','
		           + self.cross_road_id_3 + ','
		           + self.cross_road_id_4 + ')')

class Road(object):

	def __init__(self, road_id,
	             road_length,
	             road_speed,
	             road_channel,
	             road_from,
	             road_to,
	             road_isDuplex):
		self.road_id = road_id
		self.road_length = road_length
		self.road_speed = road_speed
		self.road_channel = road_channel
		self.road_from = road_from
		self.road_to = road_to
		self.road_isDuplex = road_isDuplex

	def __str__(self):
		return str('(' + self.road_id + ','
		           + str(self.road_length) + ','
		           + str(self.road_speed) + ','
		           + str(self.road_channel) + ','
		           + self.road_from + ','
		           + self.road_to + ','
		           + self.road_isDuplex + ')')

class Schedule(object):

	def __init__(self, car, start_time, road_list):
		self.road_list = road_list
		self.car = car
		self.start_time = start_time

	def __str__(self):
		roadIds = ''
		for index in range(len(self.road_list) - 1):
			roadIds += self.road_list[index].road_id + ','
		roadIds += self.road_list[-1].road_id
		return str('(' + self.car.car_id + ',' + str(self.start_time)+ ','  + roadIds +')')


