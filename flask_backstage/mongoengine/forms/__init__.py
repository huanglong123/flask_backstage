# -*- coding:utf-8 -*-
"""
表单类
"""
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, PasswordField
from wtforms import validators
from ..models import User
from .. import bcrypt


class MenuForm(FlaskForm):
	name = StringField('菜单名')
	father = SelectField('父级菜单')
	url = StringField('菜单地址')
	permissions = SelectField('菜单权限限制')
	sort = IntegerField('菜单排序')


class RoleForm(FlaskForm):
	name = StringField('角色名')
	value = IntegerField('值')


class UserForm(FlaskForm):
	username = StringField('用户名')
	password = PasswordField('密码')
	role = SelectField('角色')


class LoginForm(FlaskForm):
	username = StringField('用户名')
	password = PasswordField('密码')

	def get_user(self):
		user = User.objects(username=self.username.data).first()
		return user

	def validate_password(self, field):
		user = self.get_user()
		if user:
			if not user.password:
				raise validators.ValidationError('密码未设置')
			if not bcrypt.check_password_hash(user.password, self.password.data):
				raise validators.ValidationError('密码错误')
		else:
			raise validators.ValidationError('用户不存在')
