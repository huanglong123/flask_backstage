# -*- coding:utf-8 -*-
from flask_mongoengine import MongoEngine
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

db = MongoEngine()

THE_PERMISSIONS_CLASS = ''


class Admin(object):
	def __init__(self, app=None):
		if app is not None:
			self.init_app(app)

	def init_app(self, app):
		db.init_app(app)
		bcrypt.init_app(app)
		from flask_backstage.mongoengine.views.admin import admin
		app.register_blueprint(admin, url_prefix='/admin')
		from flask_backstage.mongoengine.models import Menu
		from flask_login import current_user

		@app.context_processor
		def menus_list():
			"""
			从数据库查询出用户有权限查看的菜单
			:return:
			"""
			if current_user.is_authenticated:
				roots = Menu.objects(father='无').order_by('sort')
				menus = []
				for r in roots:
					accessible = current_user.get_field(r.role_name) in r.permissions
					if accessible:
						menus.append({'my': r, 'child': build_child_list(r)})
					else:
						continue
				return dict(menus_list=menus)
			else:
				return dict()

		def build_child_list(r):
			childs = Menu.objects(father=r.name).order_by('sort')
			if childs:
				menus = []
				for c in childs:
					accessible = current_user.get_field(c.role_name) in c.permissions
					if accessible:
						menus.append({'my': c, 'child': build_child_list(c)})
					else:
						continue
				return menus
			else:
				return False
