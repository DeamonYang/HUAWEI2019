'''
--------------------------------------------------------
@File    :   graph.py
@Contact :   1183862787@qq.com
@License :   (C)Copyright 2017-2018, CS, WHU

@Modify Time : 2019/3/14 16:08     
@Author      : Liu Wang    
@Version     : 1.0   
@Desciption  : None
--------------------------------------------------------  
''' 
import numpy as np

MAX_INT32 = 1073741823


class Graph(object):
	"""地图"""

	def __init__(self, road_list, cross_list):

		self.__road_list = road_list
		self.__road_count = len(self.__road_list)
		self.__cross_list = cross_list
		self.__cross_count = len(self.__cross_list)

		# 定义并初始化映射
		self.__crossId_to_index = {}  # 交叉路口id到下标的映射
		for index in range(self.__cross_count):
			cross = self.__cross_list[index]
			self.__crossId_to_index[cross.cross_id] = index

		# 初始化距离矩阵D和路径矩阵P，D用于存储最短路径值，P保存路径所经过的节点
		self.__D = np.array([MAX_INT32] * (self.__cross_count * self.__cross_count), dtype='int32')
		self.__D = self.__D.reshape(-1, self.__cross_count)
		for i in range(self.__cross_count):
			self.__D[i][i] = 0      # 距离矩阵对角线元素为0
		for road in self.__road_list:
			cross_from_index = self.__crossId_to_index[road.road_from]
			cross_to_index = self.__crossId_to_index[road.road_to]
			self.__D[cross_from_index, cross_to_index] = road.road_length
			if road.road_isDuplex == '1':
				self.__D[cross_to_index, cross_from_index] = road.road_length
		# print('map:\n',self.__D.tolist())

	# Dijkstra
	def get_min_trace(self, cross_id_from, cross_id_to):
		"""
		:param cross_id_from: 起点路口的id
		:param cross_id_to: 终点路口的id
		:return: 依次经过的cross对象组成的列表
		"""
		index_from = self.__crossId_to_index[cross_id_from]
		index_to = self.__crossId_to_index[cross_id_to]
		# print('from:{},to:{}'.format(index_from, index_to))

		distance_list = self.__D[index_from].tolist()   # 存储起点到各节点最短路径值
		unvisited_distance_list = distance_list.copy()  # 存储最短距离，已访问的节点设为无穷大
		unvisited_distance_list[index_from] = MAX_INT32
		path_list = list(range(self.__cross_count))     # path_list[i]表示路径(index_from->i)所经过的节点下标
		# print('distance_list', distance_list)

		min_unvisited_distance = min(unvisited_distance_list)
		while min_unvisited_distance != MAX_INT32:
			# print('min_unvisited_distance,', min_unvisited_distance)
			index_of_min = unvisited_distance_list.index(min_unvisited_distance)
			for index in range(self.__cross_count):
				if distance_list[index] > min_unvisited_distance + self.__D[index_of_min][index]:
					distance_list[index] = min_unvisited_distance + self.__D[index_of_min][index]
					unvisited_distance_list[index] = distance_list[index]
					path_list[index] = index_of_min
			unvisited_distance_list[index_of_min] = MAX_INT32
			min_unvisited_distance = min(unvisited_distance_list)
			# print('distance_list', distance_list)
		# print(path_list)

		trace_cross_list = [ self.__cross_list[index_to] ]                       # 依次存储路线所经过的路口对象
		index_previous = path_list[index_to]
		while index_previous != path_list[index_previous]:
			trace_cross_list.append(self.__cross_list[index_previous])
			index_previous = path_list[index_previous]
		trace_cross_list.extend([self.__cross_list[index_previous], self.__cross_list[index_from]])
		trace_cross_list.reverse()
		return trace_cross_list


from reader import Reader
if __name__ == "__main__":
	reader = Reader('../config')
	graph = Graph(reader.get_roads(), reader.get_crosses())
	trace_list = graph.get_min_trace('15', '35')
	print('trace:', trace_list)
