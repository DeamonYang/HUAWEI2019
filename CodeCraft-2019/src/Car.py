'''
--------------------------------------------------------
@File    :   Car.py    
@Contact :   1183862787@qq.com
@License :   (C)Copyright 2017-2018, CS, WHU

@Modify Time : 2019/3/13 21:57     
@Author      : Liu Wang    
@Version     : 1.0   
@Desciption  : None
--------------------------------------------------------  
''' 

class Car(object):

	def __init__(self, car_id, car_from, car_to, car_speed, car_planTime):
		self.car_id = car_id
		self.car_from = car_from
		self.car_to = car_to
		self.car_speed = car_speed
		self.car_planTime = car_planTime

	def __str__(self):
		return str('(' + self.car_id + ','
		           + self.car_from + ','
		           + self.car_to + ','
		           + self.car_speed + ','
		           + self.car_planTime + ')')

