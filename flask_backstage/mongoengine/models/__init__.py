# -*- coding:utf-8 -*-

"""
封装数据库操作, 自定义元类, 定义Model组件
"""

from mongoengine import *
from flask_backstage.mongoengine import db


class Menu(db.Document):
	"""
	后台用户
	:cvar name 菜单名
	:cvar role_name 角色字段名
	:cvar father 父级菜单名
	:cvar url 对应url链接
	:cvar permissions 菜单权限限制
	:cvar sort 菜单排序
	"""
	name = StringField(required=True, unique=True)
	role_name = StringField()
	father = StringField()
	url = StringField()
	permissions = ListField()
	sort = IntField()


class Role(db.Document):
	"""
	角色
	:cvar name 角色名
	:cvar value 值
	"""
	name = StringField(required=True)
	value = IntField(required=True)

class User(db.DynamicDocument):
	username = StringField(required=True)
	password = BinaryField(required=True)
	role = IntField(required=True)
