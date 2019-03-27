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
		for road in road_list:
			self.__road_dict[road.road_id] = road

		# the schadule time
		self.__sys_clock = 0

		# total run time of all cars
		self.__total_time = 0

		# the cars arrived
		self.__arrived_list = []

		# the mapping of cross id to cross
		self.__cross_dict = {}
		for cross in cross_list:
			self.__cross_dict[cross.cross_id] = cross

		# classify schedule by start time
		self.__schedule_dict = {}
		for schedule in schedule_list:
			if str(schedule.start_time) not in self.__schedule_dict.keys():
				self.__schedule_dict[str(schedule.start_time)] = []
			self.__schedule_dict[str(schedule.start_time)].append(schedule)
		for k in self.__schedule_dict.keys():   # sort schedule list by car id
			self.__schedule_dict[k].sort(key=Schedule.get_car_id)


	def run(self):
		# 如果仍有车辆未到达终点
		while len(self.__arrived_list) != len(self.__car_list):

			self.__run_cars_in_road()

			# start the cars which are waiting in mysterious park
			self.__push_cars_to_road_from_queue()

			self.__add_cars_to_waiting_queue()

			self.__sys_clock += 1

			print('time:{},arrived count:{}'.format(self.__sys_clock, len(self.__arrived_list)))
		for v in self.__cross_dict.values():
			v.print_waiting_queue()
		pass


	def __run_cars_in_road(self):

		# 遍历道路上车辆由第一排向最后一排进行遍历，确定每辆车的行驶状态
		for road_id in self.__road_dict:
			self.__road_dict[road_id].init_cars_status()

		# 获得未处理完路口的id，并升序排序
		unsolved_crosses_id_list = list(self.__cross_dict.keys())
		unsolved_crosses_id_list.sort()
		# some cars are still in waiting status in map
		while len(unsolved_crosses_id_list) > 0:
			for cross_id in unsolved_crosses_id_list:
				# current cross to solve
				curr_cross = self.__cross_dict[cross_id]
				# move the cars which go to current cross
				self.__run_cars_by_cross(curr_cross)
				# check the status of cars which go to current cross
				solved_flag = True
				for road_id in curr_cross.road_id_list:
					if not self.__road_dict[road_id].is_solved(cross_id):
						solved_flag = False
						break
				# if the cars that go to current cross are terminal, the cross solved
				if solved_flag:
					unsolved_crosses_id_list.remove(cross_id)
			# check deadlock begin
			#
			# check deadlock end

	def __run_cars_by_cross(self, cross):
		"""
		让路口等待的车辆通过路口，并且调整相关道路上车辆的行驶状态
		:param cross: 当前路口对象
		"""
		# run cars which through cross

		# run the cars in road

	def __push_cars_to_road_from_queue(self):
		"""从路口的神奇车库中启动车辆"""
		for road_id in self.__road_dict.keys():
			# if current road has empty lane
			if True:
				self.__road_dict[road_id].pop_schedule()
		pass

	def __add_cars_to_waiting_queue(self):
		"""add the cars to cross waiting areas-mysterious park"""
		if str(self.__sys_clock + 1) in self.__schedule_dict.keys():
			# add car to cross buffer
			for schedule in self.__schedule_dict[str(self.__sys_clock + 1)]:
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

