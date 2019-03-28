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

	def get_sorted_road_id_list(self):
		road_id_list_copy = self.road_id_list.copy()
		road_id_list_copy.sort()
		return road_id_list_copy

	def get_direction(self, road_id_from, road_id_to):
		"""
		:param road_id_from: 与该路口相连的起始道路的id
		:param road_id_to: 与该路口相连的目的道路的id
		:return: 方向的代号,1代表左转，2代表直行，3代表右转，0代表掉头
		"""
		try:
			dire = (self.road_id_list.index(road_id_to) - self.road_id_list.index(road_id_from)) % 4
			return dire
		except Exception as e:
			raise Exception('Cross:{} has no road {} or {}'
			                .format(self.cross_id, road_id_from, road_id_to))


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
		self.lanes_neg = []      # 反方向的车道矩阵，矩阵元素为schedule对象
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
		如果可能过路口则设为等待，不过路口且无前车则设为停止，有前车看情况
		:param roads: [ [schedule, None, schedule, ...], [], [], ...]
		:return: roads
		"""
		for lane in lanes_list:
			for index in range(self.road_length):
				# 车道上该位置有车(调度对象)
				if lane[index] != None:
					curr_schedule = lane[index]
					v = min(lane[index].car.car_speed, self.road_speed)
					# 过路口(这里指的是当前道路不够该车行驶的情况,只考虑当前道路)
					if index - v < 0:
						# 初始状态为等待状态
						lane[index].is_terminal = False
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
							lane[index] = None
							lane[index - v] = curr_schedule
							lane[index - v].is_terminal = True
						# 前方有车阻挡
						else:
							# 阻挡车的状态为终止状态
							if lane[index_of_prev_car].is_terminal == True:
								# 前进到前方车辆的后面
								lane[index] = None
								lane[index_of_prev_car + 1] = curr_schedule
								lane[index_of_prev_car + 1].is_terminal = True
							# 阻挡车的状态为等待状态
							else:
								# 原地等待
								lane[index].is_terminal = False
				# 车道上该位置無车(调度对象)，继续看下一个位置
				else:
					continue
		return lanes_list

	def are_cars_terminal(self, cross_id):
		"""
		检测每车道第一辆车的状态是否是终止状态
		:param cross_id: 出路口的id，用来决定方向
		:return: 全终止则返回True，否则False
		"""
		terminal_flag = True
		lanes_list = self.__get_lanes_list_by_cross_id(cross_id)
		# check first car's status of each road
		for lane in lanes_list:
			for schedule in lane:
				if schedule != None:
					if schedule.is_terminal == False:
						terminal_flag = False
					break
		return terminal_flag

	def get_index_of_empty_lane(self, cross_id):
		"""
		获得可进入车道的索引
		:param cross_id: 确定是正向还是反向
		:return: 可进入车道的索引，如果均没有空车道则返回None
		"""
		lanes_list = self.__get_lanes_list_by_cross_id(cross_id)
		for lane_index in range(len(lanes_list)):
			if lanes_list[lane_index][-1] == None:
				return lane_index
		return None

	def get_first_waiting_schedule(self, cross_id, line_index):
		"""
		get the first waiting schedule in this road
		:param cross_id: to determin getting pos lanes or neg lanes
		:param index: from which line of lane to search
		:return: 1.the first waiting schedule
			2. which line of the lanes
			3. which lane of the road
		"""
		lanes_list = self.__get_lanes_list_by_cross_id(cross_id)
		for i in range(line_index, self.road_length):
			for j in range(self.road_channel):
				if lanes_list[j][i] != None:
					if not lanes_list[j][i].is_terminal:
						return lanes_list[j][i], i, j
		return None, None, None

	def __get_lanes_list_by_cross_id(self, cross_id):
		if cross_id == self.road_to:
			return self.lanes_pos
		elif cross_id == self.road_from:
			return self.lanes_neg
		else:
			raise Exception('Error param corss id:{}.'.format(cross_id))

	def go_forward_in_curr_lane(self, cross_id, lane_index, line_index):
		"""指定车辆前进,如果可能超出路口则停在路口
		:param cross_id: 连接的路口id
		:param lane_index: 车道的索引
		:param line_index: 车的起始位置,0~road_length-1,指定调度的车
		"""
		lane = self.__get_lanes_list_by_cross_id(cross_id)[lane_index]
		curr_schedule = lane[line_index]
		# 车辆在该车道最大可行驶距离
		s_max = min(curr_schedule.car.car_speed, self.road_speed, line_index)
		# 获得前车位置
		index_of_prev_car = self.get_prev_car_index(lane, line_index, s_max)
		# 前方没有车阻挡,当前车前进v路程，并设置为终止状态
		if index_of_prev_car == None:
			lane[line_index] = None
			lane[line_index - s_max] = curr_schedule
			lane[line_index - s_max].is_terminal = True
		# 前方有车阻挡
		else:
			# 阻挡车的状态为终止状态
			if lane[index_of_prev_car].is_terminal == True:
				# 前进到前方车辆的后面
				lane[line_index] = None
				lane[index_of_prev_car + 1] = curr_schedule
				lane[index_of_prev_car + 1].is_terminal = True
			# 阻挡车的状态为等待状态
			else:
				# 原地等待
				lane[line_index].is_terminal = False
		# 保存变更记录
		if cross_id == self.road_to:
			self.lanes_pos[lane_index] = lane
		else:
			self.lanes_neg[lane_index] = lane

	def get_prev_car_index(self, cross_id, lane_index, line_index, date_s):
		date_s = min(line_index, date_s)
		lane = self.__get_lanes_list_by_cross_id(cross_id)[lane_index]
		# 获得前车位置
		index_of_prev_car = None
		for j in range(date_s):
			if lane[line_index - j - 1] != None:
				index_of_prev_car = line_index - j - 1
				break
		return index_of_prev_car

	def remove_car_in_road(self, cross_id, lane_index, line_index):
		if cross_id == self.road_to:
			schedule = self.lanes_pos[lane_index][line_index]
			self.lanes_pos[lane_index][line_index] = None
			return schedule
		elif cross_id == self.road_from:
			schedule = self.lanes_neg[lane_index][line_index]
			self.lanes_neg[lane_index][line_index] = None
			return schedule
		else:
			raise Exception('Error param corss id:{}.'.format(cross_id))

	def add_car_in_road(self, cross_id, lane_index, line_index, schedule):
		"""
		添加通过路口的车辆或者从神奇车库出发的车
		:param cross_id: 从该路口驶入车辆
		:param lane_index:
		:param line_index:
		:param schedule:
		:return:
		"""
		if cross_id == self.road_to:
			self.lanes_neg[lane_index][line_index] = schedule
		elif cross_id == self.road_from:
			self.lanes_pos[lane_index][line_index] = schedule
		else:
			raise Exception('Error param corss id:{}.'.format(cross_id))

	def move_appointed_car(self, cross_id, lane_index, line_index_from, line_index_to):
		if cross_id == self.road_to:
			schedule = self.lanes_pos[lane_index][line_index_from]
			schedule.is_terminal = True
			self.lanes_pos[lane_index][line_index_from] = None
			self.lanes_pos[lane_index][line_index_to] = schedule
		elif cross_id == self.road_from:
			schedule = self.lanes_neg[lane_index][line_index_from]
			schedule.is_terminal = True
			self.lanes_neg[lane_index][line_index_from] = None
			self.lanes_neg[lane_index][line_index_to] = schedule
		else:
			raise Exception('Error param corss id:{}.'.format(cross_id))

	def push_cars_from_waiting_queue(self):
		pass

class Schedule(object):

	def __init__(self, car, start_time, road_list):
		self.road_list = road_list
		self.car = car
		self.start_time = start_time

		# self.schedule_id = car.car_id
		self.is_terminal = False  # false means waiting ,true means terminal.
		self.curr_road_index = 0

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

	def get_next_road(self):
		if self.curr_road_index + 1 < len(self.road_list):
			return self.road_list[self.curr_road_index + 1]
		else:
			return None

	def update_curr_road_index(self):
		self.curr_road_index += 1
