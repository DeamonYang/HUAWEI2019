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

	def get_speed(self):    # for sort
		return self.car_speed

	def get_planTime(self): # for sort
		return int(self.car_planTime)

	def get_Id(self):       # for sort
		return int(self.car_id)


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
		temp_list = []
		for id in self.road_id_list:
			if id != '-1':
				temp_list.append(int(id))
		temp_list.sort()
		return [str(id) for id in temp_list]

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

	def get_prev_road_id(self, curr_road_id):
		index_of_prev = (self.road_id_list.index(curr_road_id) - 1) % 4
		return self.road_id_list[index_of_prev]

	def get_next_road_id(self, curr_road_id):
		index_of_next = (self.road_id_list.index(curr_road_id) + 1) % 4
		return self.road_id_list[index_of_next]

	def get_oppo_road_id(self, curr_road_id):
		index_of_oppo = (self.road_id_list.index(curr_road_id) + 2) % 4
		return self.road_id_list[index_of_oppo]

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

	def print_lanes(self):
		print('````````````````````````````````````````````')
		print('正向')
		for i in range(len(self.lanes_pos)):
			lane = ''
			for j in range(self.road_length):
				if self.lanes_pos[i][self.road_length-j-1] == None:
					lane += '='
				else:
					lane += '*'
			print(lane)
		print('反向')
		for i in range(len(self.lanes_neg)):
			lane = ''
			for j in range(self.road_length):
				if self.lanes_neg[i][j] == None:
					lane += '='
				else:
					lane += '*'
			print(lane)
		print('.............................................')

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
		lanes_list = self.__get_lanes_list_into_cross(cross_id)
		# check first car's status of each road
		for lane in lanes_list:
			for schedule in lane:
				if schedule != None:
					if schedule.is_terminal == False:
						terminal_flag = False
					break
		return terminal_flag

	def get_index_of_empty_lane_out(self, cross_id):
		"""
		获得驶出路口的车道中可以进车的车道索引
		:param cross_id: 确定是正向还是反向
		:return: 可进入车道的索引，如果均没有空车道则返回None
		"""
		lanes_list = []
		if cross_id == self.road_from:
			lanes_list = self.lanes_pos
		elif cross_id == self.road_to:
			lanes_list = self.lanes_neg
		else:
			raise Exception('corss id error')
		for lane_index in range(len(lanes_list)):
			if lanes_list[lane_index][-1] == None:
				return lane_index
			else:
				if lanes_list[lane_index][-1].is_terminal == False:
					return lane_index
		return None

	def get_last_schedule_of_lane_out(self, cross_id, lane_index):
		"""获取驶出路口方向指定车道上最后一辆车及其位置"""
		lane = self.__get_lanes_list_outof_cross(cross_id)[lane_index]
		for i in range(self.road_length):
			if lane[self.road_length - i - 1] != None:
				return lane[self.road_length - i - 1], self.road_length - i - 1
		return None, None

	def get_first_waiting_schedule_out(self, cross_id, line_index):
		"""
		获取驶出路口方向道路上第一优先级车辆、所在车道和排索引
		:param cross_id: to determin getting pos lanes or neg lanes
		:param index: from which line of lane to search
		:return: 1.the first waiting schedule
			2. which line of the lanes
			3. which lane of the road
		"""
		lanes_list = self.__get_lanes_list_outof_cross(cross_id)
		for i in range(line_index, self.road_length):
			for j in range(self.road_channel):
				if lanes_list[j][i] != None:
					if not lanes_list[j][i].is_terminal:
						return lanes_list[j][i], i, j
		return None, None, None

	def get_first_waiting_schedule_in(self, cross_id, line_index):
		"""
		获取驶向路口方向道路上第一优先级车辆、所在车道和排索引
		:param cross_id: to determin getting pos lanes or neg lanes
		:param index: from which line of lane to search
		:return: 1.the first waiting schedule
			2. which line of the lanes
			3. which lane of the road
		"""
		lanes_list = self.__get_lanes_list_into_cross(cross_id)
		for i in range(line_index, self.road_length):
			for j in range(self.road_channel):
				if lanes_list[j][i] != None:
					if not lanes_list[j][i].is_terminal:
						return lanes_list[j][i], i, j
		return None, None, None

	def __get_lanes_list_into_cross(self, cross_id):
		"""获取驶入路口cross_id方向的车道"""
		if cross_id == self.road_to:
			return self.lanes_pos
		elif cross_id == self.road_from:
			return self.lanes_neg
		else:
			raise Exception('Error param corss id:{}.'.format(cross_id))

	def __get_lanes_list_outof_cross(self, cross_id):
		"""获取驶出路口cross_id方向的车道"""
		if cross_id == self.road_from:
			return self.lanes_pos
		elif cross_id == self.road_to:
			return self.lanes_neg
		else:
			raise Exception('Error param corss id:{}.'.format(cross_id))

	def get_prev_car_index(self, cross_id, lane_index, line_index, date_s):
		date_s = min(line_index, date_s)
		lane = self.__get_lanes_list_into_cross(cross_id)[lane_index]
		# 获得前车位置
		index_of_prev_car = None
		for j in range(date_s):
			if lane[line_index - j - 1] != None:
				index_of_prev_car = line_index - j - 1
				break
		return index_of_prev_car

	def remove_car_in_road(self, cross_id, lane_index, line_index):
		"""移除驶出路口的车辆"""
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
		schedule.is_terminal = True
		if cross_id == self.road_to:
			self.lanes_neg[lane_index][line_index] = schedule
		elif cross_id == self.road_from:
			self.lanes_pos[lane_index][line_index] = schedule
		else:
			raise Exception('Error param corss id:{}.'.format(cross_id))

	def drive_appointed_car(self, cross_id, lane_index, line_index_from, line_index_to):
		"""驱动驶向路口方向的车辆前进到指定地点"""
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

	def drive_cars_from_waiting_queue(self, cross_id):
		# 正向
		if cross_id == self.road_from:
			index_of_empty_lane = self.get_index_of_empty_lane_out(cross_id)
			while index_of_empty_lane != None and self.waiting_queue_pos.qsize() > 0:
				schedule = self.waiting_queue_pos.get()
				lane = self.lanes_pos[index_of_empty_lane]
				v_max = min(self.road_speed, schedule.car.car_speed)
				index_of_prev_car = self.road_length - v_max - 1
				for i in range(v_max):
					if lane[self.road_length-1-i] != None:
						index_of_prev_car = self.road_length-1-i
						break
				schedule.is_terminal = True
				# 驱动车库的车驶向正向车道
				self.add_car_in_road(cross_id, index_of_empty_lane, index_of_prev_car + 1, schedule)
				index_of_empty_lane = self.get_index_of_empty_lane_out(cross_id)
		elif cross_id == self.road_to:
			index_of_empty_lane = self.get_index_of_empty_lane_out(cross_id)
			while index_of_empty_lane != None and self.waiting_queue_neg.qsize() > 0:
				schedule = self.waiting_queue_neg.get()
				lane = self.lanes_neg[index_of_empty_lane]
				v_max = min(self.road_speed, schedule.car.car_speed)
				index_of_prev_car = self.road_length - v_max - 1
				for i in range(v_max):
					if lane[self.road_length - 1 - i] != None:
						index_of_prev_car = self.road_length - 1 - i
						break
				schedule.is_terminal = True
				# 驱动车库的车驶向正向车道
				self.add_car_in_road(cross_id, index_of_empty_lane, index_of_prev_car + 1, schedule)
				index_of_empty_lane = self.get_index_of_empty_lane_out(cross_id)
		else:
			raise Exception('Cross id Error')

	def push_car_to_waiting_queue(self, cross_id, schedule):
		if cross_id == self.road_from:
			self.waiting_queue_pos.put(schedule)
		elif cross_id == self.road_to:
			self.waiting_queue_neg.put(schedule)
		else:
			raise Exception('cross id Error')

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
		return int(self.car.car_id)

	def get_next_road(self):
		if self.curr_road_index + 1 < len(self.road_list):
			return self.road_list[self.curr_road_index + 1]
		else:
			return None

	def update_curr_road_index(self):
		self.curr_road_index += 1
