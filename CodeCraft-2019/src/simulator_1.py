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

from pojo import Schedule

class Simulator(object):
	""" the simulator of car running system	"""
	def __init__(self, road_list, cross_list, schedule_list):

		self.__road_dict = {}
		# the mapping of road id to road
		for road in road_list:
			self.__road_dict[road.road_id] = road
		# the mapping of cross id to cross
		self.__cross_dict = {}
		for cross in cross_list:
			self.__cross_dict[cross.cross_id] = cross
		# the mapping of car id to schedule
		self.__schedule_list = {}
		# the mapping of start time to carid-sorted schedule list
		self.__startTime_schedule_dict = {}
		for schedule in schedule_list:
			self.__schedule_list[schedule.car.car_id] = schedule
			if str(schedule.start_time) not in self.__startTime_schedule_dict.keys():
				self.__startTime_schedule_dict[str(schedule.start_time)] = []
			self.__startTime_schedule_dict[str(schedule.start_time)].append(schedule)
		for k in self.__startTime_schedule_dict.keys():   # sort schedule list by car id
			self.__startTime_schedule_dict[k].sort(key=Schedule.get_car_id)
			# for v in self.__startTime_schedule_dict[k]:
			# 	print(v)
		# the schadule time
		self.__sys_clock = 0
		# total run time of all cars
		self.__total_time = 0
		# the cars arrived
		self.__arrived_list = []
		# the waiting relationship between to schedules which are the first waiting schedule of roads
		# the key schedule wait for the value schedule
		# if there is a waiting circle, the schedules have dead lock.
		# shape => {car_id0:car_id1, ...}
		self.__waiting_dict = {}

	def run(self):
		# 如果仍有车辆未到达终点
		while len(self.__arrived_list) != len(self.__schedule_list):

			self.__add_cars_to_waiting_queue()

			self.__run_cars_in_roads()

			self.__push_cars_to_road_from_queue()

			self.__sys_clock += 1

			print('clock:{},total-time:{},arrived count:{}'.
			      format(self.__sys_clock, self.__total_time, len(self.__arrived_list)))

			# count = 0
			# for road in self.__road_dict.values():
			# 	count += road.waiting_queue_neg.qsize() + road.waiting_queue_pos.qsize()
			# print(count)

	def __run_cars_in_roads(self):

		# 遍历道路上车辆由第一排向最后一排进行遍历，初始化每辆车的行驶状态
		for road_id in self.__road_dict.keys():
			self.__road_dict[road_id].init_cars_status()

		# 初始化车辆没跑完的路口的id列表，并升序排序
		unterminal_crosses_id_list = [int(id) for id in self.__cross_dict.keys()]
		unterminal_crosses_id_list.sort()
		unterminal_crosses_id_list = [str(id) for id in unterminal_crosses_id_list]
		# some crosses are still waiting
		while len(unterminal_crosses_id_list) > 0:
			print('before:', len(unterminal_crosses_id_list))
			terminal_crosses_id_list = []
			for cross_id in unterminal_crosses_id_list:
				# current cross to solve
				curr_cross = self.__cross_dict[cross_id]
				# move the cars which go to current cross
				terminal_flag = self.__run_cars_by_cross(curr_cross)
				# if the cars that go to current cross are terminal, the cross become terminal
				if terminal_flag:
					# add cross_id to 'terminal_crosses_id_list'
					terminal_crosses_id_list.append(cross_id)
			# refresh 'unterminal_crosses_id_list'
			unterminal_crosses_id_list = list(set(unterminal_crosses_id_list) - set(terminal_crosses_id_list))
			unterminal_crosses_id_list = [int(id) for id in unterminal_crosses_id_list]
			unterminal_crosses_id_list.sort()
			unterminal_crosses_id_list = [str(id) for id in unterminal_crosses_id_list]
			print('after:', len(unterminal_crosses_id_list))
			# check deadlock begin
			if self.__has_dead_lock():
				raise Exception('has dead lock')
			# check deadlock end

	def __run_cars_by_cross(self, curr_cross):
		"""
		让路口等待的车辆通过路口，并且调整相关道路上车辆的行驶状态
		:param cross: 当前路口对象
		:return 返回驶向当前路口的车是否都终止
		"""
		# print('run cars by cross:{}'.format(curr_cross))
			# 循环调度路口的道路
		for curr_road_id in curr_cross.get_sorted_road_id_list():
			# current road : self.__road_dict[road_id]
			# s形顺序处理当前道路上的车辆
			line_index, lane_index = 0, 0
			while line_index != None:
				# get the first waiting schedule
				schedule, line_index, lane_index = self.__road_dict[curr_road_id].get_first_waiting_schedule_in(
					curr_cross.cross_id, line_index
				)
				# 该道路调度未完成，仍有等待过路口的车辆
				if schedule != None:
					# 获取下一个要走的道路对象,如果为None则表示已经是最后一条道路即前方为终点
					next_road = schedule.get_next_road()
					# 前方路口为终点
					if next_road == None:
						# 从道路上移除该车，并加入到已到达列表
						self.__arrived_list.append(
							self.__road_dict[curr_road_id].remove_car_in_road(
								curr_cross.cross_id, lane_index, line_index
							)
						)
						self.__total_time += self.__sys_clock - schedule.car.car_planTime
						self.__del_waiting_relation(schedule.car.car_id)
					# 前方路口不是终点，可能需要通过路口
					else:
						# 获取下一道路可行车速
						v_max_next_road = min(schedule.car.car_speed, next_road.road_speed)
						# 下条道路可行车速不超过当前道路可行距离,不通过路口,行驶至第一排
						if v_max_next_road <= line_index:
							self.__road_dict[curr_road_id].drive_appointed_car(
								curr_cross.cross_id, lane_index, line_index, 0
							)
							self.__del_waiting_relation(schedule.car.car_id)
						# 下一道路可行车速够大，满足过路口条件
						else:
							# 冲突判定, 与当前车冲突的车辆的id
							conflict_car_id = None
							# 获取当前车的转弯编号
							curr_dir = curr_cross.get_direction(curr_road_id, next_road.road_id)
							# 直行
							if curr_dir == 2:
								pass
							# 左转
							elif curr_dir == 1:
								prev_road_id = curr_cross.get_prev_road_id(curr_road_id)
								if prev_road_id != '-1':
									prev_road_first_schedule, _, _ = \
										self.__road_dict[prev_road_id].get_first_waiting_schedule_in(
										curr_cross.cross_id, 0
									)
									if prev_road_first_schedule != None:
										temp_road = prev_road_first_schedule.get_next_road()
										if temp_road == None:   # 终点直行
											conflict_car_id = prev_road_first_schedule.car.car_id
										else:
											temp_dir = curr_cross.get_direction(prev_road_id, temp_road.road_id)
											if temp_dir == 2:
												conflict_car_id = prev_road_first_schedule.car.car_id
							# 右转
							elif curr_dir == 3:
								# 判断是否有直行驶入
								next_road_id = curr_cross.get_next_road_id(curr_road_id)
								if next_road_id != '-1':
									next_road_first_schedule, _, _ = \
										self.__road_dict[next_road_id].get_first_waiting_schedule_in(
											curr_cross.cross_id, 0
										)
									if next_road_first_schedule != None:
										temp_road = next_road_first_schedule.get_next_road()
										if temp_road == None:   # 去终点为直行
											conflict_car_id = next_road_first_schedule.car.car_id
										else:
											temp_dir = curr_cross.get_direction(next_road_id, temp_road.road_id)
											if temp_dir == 2:
												conflict_car_id = next_road_first_schedule.car.car_id
								# 判断是否有左转驶入
								oppo_road_id = curr_cross.get_oppo_road_id(curr_road_id)
								if oppo_road_id != '-1':
									oppo_road_first_schedule, _, _ = \
										self.__road_dict[oppo_road_id].get_first_waiting_schedule_in(
											curr_cross.cross_id, 0
										)
									if oppo_road_first_schedule != None:
										temp_road = oppo_road_first_schedule.get_next_road()
										if temp_road != None:
											temp_dir = curr_cross.get_direction(oppo_road_id, temp_road.road_id)
											if temp_dir == 1:
												conflict_car_id = oppo_road_first_schedule.car.car_id
							else:
								raise Exception('direction error')

							# 发生冲突，跳过当前车道调度
							if conflict_car_id != None:
								# 冲突车辆被下一道路堵死,则当前车也被堵死
								self.__add_waiting_relation(schedule.car.car_id, conflict_car_id)
								break
							# 没有冲突，看下一道路车辆状况
							else:
								# 出路口方向的第一个空车道
								index_empty_lane = self.__road_dict[next_road.road_id].\
									get_index_of_empty_lane_out(curr_cross.cross_id)
								# 無空闲车道（道路上满车且所有车都进入终止状态）
								if index_empty_lane == None:
									# 行驶至第一排
									self.__road_dict[curr_road_id].drive_appointed_car(
										curr_cross.cross_id, lane_index, line_index, 0
									)
									self.__del_waiting_relation(schedule.car.car_id)
								# 有空闲车道
								else:
									# 空闲车道上最后一辆车及其位置
									temp_schedule, temp_line_index = self.__road_dict[next_road.road_id].\
										get_last_schedule_of_lane_out(curr_cross.cross_id, index_empty_lane)
									# 下一条道路没有车的情况下可行驶距离
									s_next_road = v_max_next_road - line_index
									# 下一车道可行距离大于0,进入下一车道或者等待
									if s_next_road > 0:
										# 空闲车道没有车或者空闲车道上的车没有挡住当前车进入
										if temp_schedule == None or s_next_road<next_road.road_length-temp_line_index:
											# 过路口并行驶最大距离
											self.__road_dict[curr_road_id].remove_car_in_road(
												curr_cross.cross_id, lane_index, line_index
											)
											schedule.update_curr_road_index()
											self.__road_dict[next_road.road_id].add_car_in_road(
												curr_cross.cross_id, index_empty_lane,
												next_road.road_length-s_next_road, schedule
											)
											self.__del_waiting_relation(schedule.car.car_id)
										# 空闲车道上最后一辆车挡住当前车驶入
										else:
											# 挡道车辆为终止状态则行驶至其后
											if temp_schedule.is_terminal == True:
												# 过路口并行驶至前车之后
												self.__road_dict[curr_road_id].remove_car_in_road(
													curr_cross.cross_id, lane_index, line_index
												)
												schedule.update_curr_road_index()
												self.__road_dict[next_road.road_id].add_car_in_road(
													curr_cross.cross_id, index_empty_lane,
													temp_line_index + 1, schedule
												)
												self.__del_waiting_relation(schedule.car.car_id)
											# 挡道车为等待状态则保持不动
											else:
												# 当前车保持等待状态
												# first waiting schedule of next road
												fwsonr, _, _ = self.__road_dict[next_road.road_id].\
													get_first_waiting_schedule_out(curr_cross.cross_id, 0)
												# 新增等待关系
												self.__add_waiting_relation(schedule.car.car_id, fwsonr.car.car_id)
												break
									# 下一车道可行距离小于等于0,驶向当前车道第一排
									else:
										self.__road_dict[curr_road_id].drive_appointed_car(
											curr_cross.cross_id, lane_index, line_index, 0
										)
										self.__del_waiting_relation(schedule.car.car_id)
		# check the status of cars which go to current cross
		# if all cars in the 4 roads become terminal ,return true. If not, return False
		terminal_flag = True
		for road_id in curr_cross.get_sorted_road_id_list():
			if not self.__road_dict[road_id].are_cars_terminal(curr_cross.cross_id):
				terminal_flag = False
				break
		return terminal_flag

	def __push_cars_to_road_from_queue(self):
		"""从路口的神奇车库中启动车辆"""
		for cross in self.__cross_dict.values():
			road_id_list = cross.get_sorted_road_id_list()
			for road_id in road_id_list:
				self.__road_dict[road_id].drive_cars_from_waiting_queue(cross.cross_id)
		pass

	def __add_cars_to_waiting_queue(self):
		"""add the cars to cross waiting areas-mysterious park"""
		if str(self.__sys_clock) in self.__startTime_schedule_dict.keys():
			# add car to cross buffer
			for schedule in self.__startTime_schedule_dict[str(self.__sys_clock)]:
				# print(schedule)
				# 起点非终点
				if len(schedule.road_list) > 0:
					# id of the first road
					first_road_id = schedule.road_list[0].road_id
					cross_id_from = schedule.car.car_from
					# push schedule object to waiting queue
					self.__road_dict[first_road_id].push_car_to_waiting_queue(cross_id_from, schedule)
				# 起点即终点
				else:
					self.__arrived_list.append(schedule)

	def __add_waiting_relation(self, car_id_1, car_id_2):
		self.__waiting_dict[car_id_1] = car_id_2

	def __del_waiting_relation(self, car_id_1):
		if car_id_1 in self.__waiting_dict.keys():
			self.__waiting_dict.pop(car_id_1)

	def __has_dead_lock(self):
		return False