'''
--------------------------------------------------------
@File    :   Road.py    
@Contact :   1183862787@qq.com
@License :   (C)Copyright 2017-2018, CS, WHU

@Modify Time : 2019/3/13 22:03     
@Author      : Liu Wang    
@Version     : 1.0   
@Desciption  : None
--------------------------------------------------------  
''' 
class Road(object):

	def __init__(self, road_id, road_length, rood_speed, rood_channel, rood_from, rood_to, rood_isDuplex):
		self.road_id = road_id
		self.road_length = road_length
		self.rood_speed = rood_speed
		self.rood_channel = rood_channel
		self.rood_from = rood_from
		self.rood_to = rood_to
		self.rood_isDuplex = rood_isDuplex