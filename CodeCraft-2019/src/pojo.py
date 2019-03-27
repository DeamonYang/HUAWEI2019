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
import queue

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

		self.is_terminal = False         # false means waiting ,ture means terminal.

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


class Cross(object):

	def __init__(self, cross_id,
	             road_id_1,
	             road_id_2,
	             road_id_3,
	             road_id_4):
		self.cross_id = cross_id
		self.road_id_list = [road_id_1, road_id_2, road_id_3, road_id_4]

	def __str__(self):
		return str('(' + self.cross_id + ','
		           + self.road_id_list[0] + ','
		           + self.road_id_list[1] + ','
		           + self.road_id_list[2] + ','
		           + self.road_id_list[3] + ')')

	# def print_waiting_queue(self):
	# 	for que in self.waiting_queue_dict:
	# 		print(' ********************* ')
	# 		while que.empty() != True:
	# 			print(que.get())
	# 	print('=================================')
	#
	# def push_schedule(self, road_id, schedule_obj):
	# 	self.waiting_queue_dict[road_id].put(schedule_obj)
	#
	# def pop_schedule(self, road_id):
	# 	schedule = self.waiting_queue_dict[road_id].get()
	# 	return schedule


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

		# 初始化道路的车位列表
		self.lanes_pos = []      # 正方向的车道矩阵，矩阵元素为schedule对象
		self.lanes_neg = []      # 反方向的车道，矩阵元素为schedule对象
		for index in range(self.road_channel):
			self.lanes_pos.append([None] * road_length)
		if self.road_isDuplex:
			for index in range(self.road_channel):
				self.lanes_neg.append([None] * road_length)

		# the element of queue is Schedule obj
		self.waiting_queue_pos = queue.Queue()      # 正向神奇车库发车区
		self.waiting_queue_neg = queue.Queue()      # 反向神奇车库发车区

	def __str__(self):
		return str('(' + self.road_id + ','
		           + str(self.road_length) + ','
		           + str(self.road_speed) + ','
		           + str(self.road_channel) + ','
		           + self.road_from + ','
		           + self.road_to + ','
		           + self.road_isDuplex + ')')


	def init_cars_status(self):
		"""设置该时刻两个方向车道上车辆的初始状态"""
		self.lanes_pos = self.__init_cars_status(self.lanes_pos)
		self.lanes_neg = self.__init_cars_status(self.lanes_neg)

	def __init_cars_status(self, lanes_list):
		"""设置该时刻指定车道上车辆的初始状态
		:param roads: [ [schedule, None, schedule, ...], [], [], ...]
		:return: roads
		"""
		for lane in lanes_list:
			for index in range(self.road_length):
				# 车道上该位置有车(调度对象)
				if lane[index] != None:
					v = min(lane[index].car.car_speed, self.road_speed)
					# 过路口
					if index - v < 0:
						# 初始状态为等待状态
						lane[index].car.is_terminal = False
					# 不过路口
					else:
						# 获得前车位置
						index_of_prev_car = None
						for j in range(v):
							if lane[index - j - 1] != None:
								index_of_prev_car = index - j - 1
								break
						# 前方没有车阻挡,当前车前进v路程，并设置为终止状态
						if index_of_prev_car == None:
							curr_schedule = lane[index]
							lane[index] = None
							lane[index - v] = curr_schedule
							lane[index].car.is_terminal = True
						# 前方有车阻挡
						else:
							# 阻挡车的状态为终止状态
							if lane[index_of_prev_car].car.is_terminal == True:
								# 前进到前方车辆的后面
								curr_schedule = lane[index]
								lane[index] = None
								lane[index_of_prev_car + 1] = curr_schedule
							# 阻挡车的状态为等待状态
							else:
								# 原地等待
								lane[index].car.is_terminal = False
				# 车道上该位置無车(调度对象)，继续看下一个位置
				else:
					continue
		return lanes_list

	def is_solved(self, cross_id):
		"""
		检测每车道第一辆车的状态是否是终止状态
		:param cross_id: 出路口的id，用来决定方向
		:return: 全终止则返回True，否则False
		"""
		solved_flag = True
		lanes_list = self.__get_lanes_list_by_cross_id(cross_id)
		# check first car's status of each road
		for lane in lanes_list:
			for car in lane:
				if car != None:
					if car.is_terminal == False:
						solved_flag = False
					break
		return solved_flag

	def has_empty_lane(self, cross_id):
		lanes_list = self.__get_lanes_list_by_cross_id(cross_id)
		for lane in lanes_list:
			if lane[-1] == None:
				return True
		return False

	def __get_lanes_list_by_cross_id(self, cross_id):
		if cross_id == self.road_to:
			return self.lanes_pos
		elif cross_id == self.road_from:
			return self.lanes_neg
		else:
			raise Exception('Error param corss id:{}.'.format(cross_id))



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
