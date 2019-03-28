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
	def __init__(self, car_list, road_list, cross_list, schedule_list):

		self.__car_list = car_list
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
		while len(self.__arrived_list) != len(self.__car_list):

			self.__run_cars_in_roads()

			# start the cars which are waiting in mysterious park
			self.__push_cars_to_road_from_queue()

			self.__add_cars_to_waiting_queue()

			self.__sys_clock += 1

			print('time:{},arrived count:{}'.format(self.__sys_clock, len(self.__arrived_list)))
		for v in self.__cross_dict.values():
			v.print_waiting_queue()
		pass


	def __run_cars_in_roads(self):

		# 遍历道路上车辆由第一排向最后一排进行遍历，初始化每辆车的行驶状态
		for road_id in self.__road_dict:
			self.__road_dict[road_id].init_cars_status()

		# 初始化车辆没跑完的路口的id列表，并升序排序
		unterminal_crosses_id_list = list(self.__cross_dict.keys())
		unterminal_crosses_id_list.sort()
		# some crosses are still waiting
		while len(unterminal_crosses_id_list) > 0:
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
			# check deadlock begin
			#
			# check deadlock end

	def __run_cars_by_cross(self, curr_cross):
		"""
		让路口等待的车辆通过路口，并且调整相关道路上车辆的行驶状态
		:param cross: 当前路口对象
		:return 返回当前路口是否处理完毕(朝当前入口驶入的车辆是否都到达终止状态)
		"""
		# # 循环调度路口的道路
		sorted_unsolved_road_id_list = curr_cross.get_sorted_road_id_list()
		while len(sorted_unsolved_road_id_list) > 0:
			# id of the roads whose cars are terminal or waiting the car which is in waiting status of next road
			solved_road_id_list = []
			for curr_road_id in sorted_unsolved_road_id_list:
				# current road : self.__road_dict[road_id]
				line_index, lane_index = 0, 0
				while line_index != None:
					# get the first waiting schedule
					schedule, line_index, lane_index = self.__road_dict[curr_road_id].get_first_waiting_schedule(
						curr_cross.cross_id, line_index
					)
					# 该道路调度未完成，仍有等待行驶的车辆
					if schedule != None:
						# 当前道路最大车速
						v_max_curr_road = min(schedule.car.car_speed, self.__road_dict[curr_road_id].road_speed)
						# 可行车速大于当前道路剩余的路程，可能需要过路口
						if line_index < v_max_curr_road:
							# 获取下一条道路的对象
							next_road = schedule.get_next_road()
							# 前方路口为终点，不用通过路口
							if next_road == None:
								index_of_prev_car = self.__road_dict[curr_road_id].get_prev_car_index(
									curr_cross.cross_id, lane_index, line_index
								)
								# 前方无车阻挡
								if index_of_prev_car != None:
									self.__road_dict[curr_road_id].remove_car_in_road(
										curr_cross.cross_id, lane_index, line_index
									)
									# 抵达终点
									self.__arrived_list.append(schedule)
								# 前方有车阻挡
								else:
									self.__road_dict[curr_road_id].go_forward_in_curr_lane(
										curr_cross.cross_id, lane_index, line_index
									)
							# 前方路口不是终点，可能需要通过路口
							else:
								# 下条路最大车速，用来参与决定该车是否可以过路口
								v_max_next_road = min(schedule.car.car_speed, next_road.road_speed)

						# 一定不需要过路口
						else:
							# 前进 v_max_curr_road 单位，或者停在前车后一个位置
							self.__road_dict[curr_road_id].go_forward_in_curr_lane(
								curr_cross.cross_id, lane_index, line_index
							)

					# 该道路调度完成
					else:
						solved_road_id_list.append(curr_road_id)


				conflict = False
				if conflict or line_index == None:
					solved_road_id_list.append(road_id)

			sorted_unsolved_road_id_list = list(set(sorted_unsolved_road_id_list) - set(solved_road_id_list))



		# check the status of cars which go to current cross
		# if all cars in the 4 roads become terminal ,return true. If not, return False
		terminal_flag = True
		for road_id in curr_cross.road_id_list:
			if not self.__road_dict[road_id].are_cars_terminal(curr_cross.cross_id):
				terminal_flag = False
				break
		return terminal_flag

	def __push_cars_to_road_from_queue(self):
		"""从路口的神奇车库中启动车辆"""
		for road_id in self.__road_dict.keys():
			# if current road has empty lane
			if True:
				self.__road_dict[road_id].pop_schedule()
		pass

	def __add_cars_to_waiting_queue(self):
		"""add the cars to cross waiting areas-mysterious park"""
		if str(self.__sys_clock + 1) in self.__startTime_schedule_dict.keys():
			# add car to cross buffer
			for schedule in self.__startTime_schedule_dict[str(self.__sys_clock + 1)]:
				# 起点非终点
				if len(schedule.road_list) > 0:
					# id of the first road
					road_id_0 = schedule.road_list[0].road_id
					# push schedule object to waiting queue
					# ...
				# 起点即终点
				else:
					self.__arrived_list.append(schedule)
				self.__arrived_list.append(schedule)
		pass


# # 官方路口处理伪代码
# for (/ * 按时间片处理 * /) {
# 	while (/ * all car in road run into end state * /){
# 		foreach(roads) {
# 			/ * 调整所有道路上在道路上的车辆，让道路上车辆前进，只要不出路口且可以到达终止状态的车辆
# 			* 分别标记出来等待的车辆（要出路口的车辆，或者因为要出路口的车辆阻挡而不能前进的车辆）
# 			* 和终止状态的车辆（在该车道内可以经过这一次调度可以行驶其最大可行驶距离的车辆） * /
# 			driveAllCarJustOnRoadToEndState(allChannle); / * 对所有车道进行调整 * /
#
# 			/ * driveAllCarJustOnRoadToEndState该处理内的算法与性能自行考虑 * /
# 		}
# 	}
#
# 	while (/ * all car in road run into end state * /){
# 		/ * driveAllWaitCar() * /
# 		foreach(crosses){
# 			foreach(roads){
# 				while (/ * wait car on the road * /){
# 					Direction dir = getDirection();
# 					Car car = getCarFromRoad(road, dir);
# 					if (conflict){
# 						break;
# 					}
#
# 					channle = car.getChannel();
# 					car.moveToNextRoad();
#
# 					/ *driveAllCarJustOnRoadToEndState该处理内的算法与性能自行考虑 * /
# 				   driveAllCarJustOnRoadToEndState(channel);
# 				}
# 			}
# 		}
# 	}
# }

