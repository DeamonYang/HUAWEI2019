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

		self.is_checked = False     # in this clock, false means unchecked, true means checked.
		self.status = False         # in this clock, false means waiting , ture means terminal.

	def __str__(self):
		return str('(' + self.car_id + ','
		           + self.car_from + ','
		           + self.car_to + ','
		           + str(self.car_speed) + ','
		           + str(self.car_planTime) + ')')

	def get_speed(self):
		return self.car_speed

	def get_planTime(self):     # for sort
		return self.car_planTime

	def get_Id(self):       # for sort
		return self.car_id




import queue

class Cross(object):

	def __init__(self, cross_id,
	             cross_road_id_1,
	             cross_road_id_2,
	             cross_road_id_3,
	             cross_road_id_4):
		self.cross_id = cross_id
		self.road_id_list = [cross_road_id_1, cross_road_id_2, cross_road_id_3, cross_road_id_4]
		self.waiting_list = [queue.Queue(), queue.Queue(), queue.Queue(), queue.Queue()]        # cross buffer

	def __str__(self):
		return str('(' + self.cross_id + ','
		           + self.road_id_list[0] + ','
		           + self.road_id_list[1] + ','
		           + self.road_id_list[2] + ','
		           + self.road_id_list[3] + ')')

	def print_waiting_queue(self):
		for que in self.waiting_list:
			print(' ********************* ')
			while que.empty() != True:
				print(que.get())
		print('=================================')


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

		# self.are_cars_waiting = True

		# 初始化道路的车位列表
		self.roads_pos = []      # 正方向的车道矩阵，矩阵元素为schedule对象
		self.roads_neg = []      # 反方向的车道，矩阵元素为schedule对象
		for index in range(self.road_channel):
			self.roads_pos.append([None] * road_length)
		if self.road_isDuplex:
			for index in range(self.road_channel):
				self.roads_neg.append([None] * road_length)

	def __str__(self):
		return str('(' + self.road_id + ','
		           + str(self.road_length) + ','
		           + str(self.road_speed) + ','
		           + str(self.road_channel) + ','
		           + self.road_from + ','
		           + self.road_to + ','
		           + self.road_isDuplex + ')')


	def init_cars_status(self):
		self.roads_pos = self.__init_cars_status(self.roads_pos)
		self.roads_neg = self.__init_cars_status(self.roads_neg)

	def __init_cars_status(self, roads):
		"""设置该时刻车辆的初始状态
		:param roads: [ [schedule, None, schedule, ...], [], [], ...]
		:return: roads
		"""
		for road in roads:
			for index in range(self.road_length):
				if road[index] != None:         # 车道上该位置有车(调度对象)
					v = min(road[index].car.car_speed, self.road_speed)
					if index - v < 0:           # 过路口
						road[index].car.status = False      # 过路口初始状态为等待状态
					else:   # 不过路口
						index_of_prev_car = None
						for j in range(v):
							if road[index - j - 1] != None:
								index_of_prev_car = index - j - 1
								break
						if index_of_prev_car == None:   # 没有车阻挡,当前车前进v路程，并设置为终止状态
							curr_schedule = road[index]
							road[index] = None
							road[index - v] = curr_schedule
							road[index].car.status = True
						else:   # 前方有车阻挡
							if road[index_of_prev_car].car.status == True: # 阻挡车的状态为终止状态
								# 前进到前方车辆的后面
								curr_schedule = road[index]
								road[index] = None
								road[index_of_prev_car + 1] = curr_schedule
							else:   # 阻挡车的状态为等待状态
								# 原地等待
								road[index].car.status = False
					road[index].car.is_checked = True
				else: # 车道上该位置無车(调度对象)，继续看下一个位置
					continue
		return roads

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

	def get_start_time(self):   # for sort
		return self.start_time

	def get_car_id(self):       # for sort
		return self.car.car_id
