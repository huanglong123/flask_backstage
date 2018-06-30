# -*- coding:utf-8 -*-
from flask_mongoengine import MongoEngine
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect

#数据库
db = MongoEngine()

# 安全组件
csrf = CSRFProtect()
bcrypt = Bcrypt()

class Admin(object):
	def __init__(self, app=None):
		if app is not None:
			self.init_app(app)

	def init_app(self, app):
		if app.config.get('SECRET_KEY', None) is None:
			app.config['SECRET_KEY'] = 'admin'
		db.init_app(app)  # 数据库
		# 安全组件
		csrf.init_app(app)  # 全站开通csrf保护,配置文件需要启用
		bcrypt.init_app(app)  # 密码加密组件
		from .views.admin import admin
		app.register_blueprint(admin, url_prefix='/admin')
		from .models import Menu, User, Role
		from flask_login import LoginManager
		login_manager = LoginManager()
		login_manager.init_app(app)  # 用于用户的登录，登出和登录访问控制

		login_manager.login_view = "admin.login"

		@login_manager.user_loader
		def load_user(user_id):
			return User.objects(id=user_id).first()

		from flask_login import current_user
		admin = User.objects(role=300).first()
		role = Role.objects(value=300).first()
		if not admin:
			user = User()
			user.username = 'admin'
			user.password = bcrypt.generate_password_hash('123456')
			user.role = 300
			user.save()
		if not role:
			role = Role()
			role.name = '超级管理员'
			role.value = 300
			role.save()

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
					accessible = current_user.role in r.permissions
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
					accessible = current_user.role in c.permissions
					if accessible:
						menus.append({'my': c, 'child': build_child_list(c)})
					else:
						continue
				return menus
			else:
				return False
