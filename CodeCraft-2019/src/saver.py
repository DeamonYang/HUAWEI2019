'''
--------------------------------------------------------
@File    :   saver.py    
@Contact :   1183862787@qq.com
@License :   (C)Copyright 2017-2018, CS, WHU

@Modify Time : 2019/3/15 19:17     
@Author      : Liu Wang    
@Version     : 1.0   
@Desciption  : None
--------------------------------------------------------  
''' 


class Saver(object):

	def __init__(self, answer_file, schedule_list):
		self.__answer_file = answer_file
		self.__schedule_list = schedule_list

	def save(self):
		with open(self.__answer_file, 'w', encoding='utf-8') as answer_file:
			lines = list()
			lines.append('#(carId,StartTime,RoadId1,RoadId2...)\n')
			for schedule in self.__schedule_list:
				lines.append(str(schedule)+'\n')
			answer_file.writelines(lines)