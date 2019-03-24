'''
--------------------------------------------------------
@File    :   simulator.py    
@Contact :   1183862787@qq.com
@License :   (C)Copyright 2017-2018, CS, WHU

@Modify Time : 2019/3/22 15:38     
@Author      : Liu Wang    
@Version     : 1.0   
@Desciption  : None
--------------------------------------------------------  
''' 

class Simulator(object):


	def __init__(self, car_list, road_list, cross_list, schedule_list):

		self.__car_list = car_list
		self.__road_list = road_list
		self.__cross_list = cross_list
		self.__schedule_list = schedule_list    # the result of the dispatcher
		self.__schedule_time = 0                 # the schadule time
		self.__total_time = 0               # total run time of all cars
		self.__car_arrived_list = []        # the cars arrived

		self.__startTime_to_schedules = {}      # classify schedule by start time
		for schedule in self.__schedule_list:
			if schedule.start_time not in self.__startTime_to_schedules.keys():
				self.__startTime_to_schedules[str(schedule.start_time)] = []
			self.__startTime_to_schedules[str(schedule.start_time)].append(schedule)

		self.__crossId_to_cross = {}        # the mapping of cross id to cross
		for cross in self.__cross_list:
			self.__crossId_to_cross[cross.cross_id] = cross


	def run(self):
		while len(self.__car_arrived_list) != len(self.__car_list):
			self.__run_a_clock()
			self.__schedule_time += 1

	def __run_a_clock(self):
		self.__add_waiting_cars_to_cross()
		self.__go_forward()
		pass

	def __add_waiting_cars_to_cross(self):
		"""add the cars to cross waiting areas-mysterious park"""
		for schedule in self.__startTime_to_schedules[str(self.__schedule_time + 1)]:
			pass

	def __go_forward(self):
		pass
