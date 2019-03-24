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
		self.__schedule_list = schedule_list
		self.__run_time = 0
		self.__total_time = 0

	def run(self):



		self.__run_time += 1

