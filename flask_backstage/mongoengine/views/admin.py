# -*- coding:utf-8 -*-
"""
子目录统一使用带/的url风格,如:@apps.route('/projects/'), methods默认是get和head
Blueprint 注册, 使用范例:
frontend = Blueprint('frontend',  # 注册蓝图名称
        __name__,
        template_folder='/opt/auras/templates/',   # 指定模板路径
        static_folder='/opt/auras/flask_bootstrap/static/',# 指定静态文件路径
                   )
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from ..models import Menu, Role, User
from ..forms import MenuForm, RoleForm, LoginForm, UserForm
from flask_login import login_required, logout_user, login_user
from ..utils.helps import admin_create_required
from .. import bcrypt

admin = Blueprint('admin', __name__, template_folder='../templates', static_folder='../static')

admin_required = admin_create_required(300)



@admin.route('/', methods=('GET', 'POST'))
def login():
	"""
	登录
	:return:
	"""
	form = LoginForm()
	if form.validate_on_submit():
		login_user(form.get_user())
		return redirect(url_for('admin.menu_list'))
	return render_template('admin/login.html', form=form)


@admin.route('/login_out/', methods=('GET', 'POST'))
@login_required
def login_out():
	"""
	退出登录
	:return:
	"""
	logout_user()
	return redirect(url_for('admin.login'))


@admin.route('/menu_list/', methods=('GET', 'POST'))
@login_required
@admin_required
def menu_list():
	"""
	进入菜单列表
	:return:
	"""
	menus = Menu.objects
	return render_template('admin/menu_list.html', menus=menus)


@admin.route('/menu_add/', methods=('GET', 'POST'))
@login_required
@admin_required
def menu_add():
	"""
	添加菜单
	:return:
	"""
	form = MenuForm()
	menus = Menu.objects
	roles = Role.objects
	form.father.choices = [('无', '无')] + [(m.name, m.name) for m in menus]
	form.permissions.choices = [(0, '默认权限')] + [(r.value, r.name) for r in roles]
	return render_template('admin/menu_add.html', form=form)


@admin.route('/menu_save/', methods=('GET', 'POST'))
@login_required
@admin_required
def menu_save():
	"""
	保存菜单
	:return:
	"""
	form = MenuForm()
	menu = Menu()
	form.populate_obj(menu)
	permissions = request.form.get('permissions').split(",")[0:-1]
	permissions = list(map(int, permissions))
	menu.permissions = permissions
	menu.save()
	return redirect(url_for('admin.menu_list'))


@admin.route('/menu_edit/<string:mid>/', methods=('GET', 'POST'))
@login_required
@admin_required
def menu_edit(mid):
	"""
	编辑菜单
	:param mid:
	:return:
	"""
	menu = Menu.objects(id=mid).first()
	roles = Role.objects
	form = MenuForm()
	menus = Menu.objects
	form.father.choices = [('无', '无')] + [(m.name, m.name) for m in menus]
	form.name.data = menu.name
	form.father.data = menu.father
	form.url.data = menu.url
	form.permissions.choices = [(0, '默认权限')] + [(r.value, r.name) for r in roles]
	form.sort.data = menu.sort
	permissions = ",".join(list(map(str, menu.permissions))) + ","

	return render_template('admin/menu_edit.html', form=form, menu=menu, permissions=permissions)


@admin.route('/menu_editsave/', methods=('GET', 'POST'))
@login_required
@admin_required
def menu_editsave():
	"""
	保存编辑的菜单
	:return:
	"""
	mid = request.form.get('mid')
	form = MenuForm()
	menu = Menu.objects(id=mid).first()
	permissions = request.form.get('permissions').split(",")[0:-1]
	permissions = list(map(int, permissions))
	form.populate_obj(menu)
	menu.permissions = permissions
	menu.save()
	return redirect(url_for('admin.menu_list'))


@admin.route('/menu_del/<string:mid>/', methods=('GET', 'POST'))
@login_required
@admin_required
def menu_del(mid):
	"""
	删除菜单
	:param mid:
	:return:
	"""
	menu = None
	if mid:
		menu = Menu.objects(id=mid).first()
	if not menu:
		flash(u'对不起，角色不存在或已经删除')
	else:
		menu.delete()
		flash(u'删除角色成功')
	return redirect(url_for('admin.menu_list'))


@admin.route('/role_list', methods=('GET', 'POST'))
@login_required
@admin_required
def role_list():
	"""
	角色列表
	:return:
	"""
	roles = Role.objects
	return render_template('admin/role_list.html', roles=roles)


@admin.route('/role_add/', methods=('GET', 'POST'))
@login_required
@admin_required
def role_add():
	"""
	添加角色
	:return:
	"""
	form = RoleForm()
	return render_template('admin/role_add.html', form=form)


@admin.route('/role_save/', methods=('GET', 'POST'))
@login_required
@admin_required
def role_save():
	"""
	角色保存
	:return:
	"""
	form = RoleForm()
	role = Role()
	form.populate_obj(role)
	role.save()
	return redirect(url_for('admin.role_list'))


@admin.route('/role_edit/<string:rid>/', methods=('GET', 'POST'))
@login_required
@admin_required
def role_edit(rid):
	"""
	编辑角色
	:param rid:
	:return:
	"""
	role = Role.objects(id=rid).first()
	form = RoleForm()
	form.name.data = role.name
	form.value.data = role.value
	return render_template('admin/role_edit.html', form=form, role=role)


@admin.route('/role_editsave/', methods=('GET', 'POST'))
@login_required
@admin_required
def role_editsave():
	"""
	保存角色编辑
	:return:
	"""
	rid = request.form.get('rid')
	form = RoleForm()
	role = Role.objects(id=rid).first()
	form.populate_obj(role)
	role.save()
	return redirect(url_for('admin.role_list'))


@admin.route('/role_del/<string:rid>/', methods=('GET', 'POST'))
@login_required
@admin_required
def role_del(rid):
	"""
	删除角色
	:param rid:
	:return:
	"""
	role = None
	if rid:
		role = Role.objects(id=rid).first()
	if not role:
		flash(u'对不起，角色不存在或已经删除')
	else:
		role.delete()
		flash(u'删除角色成功')
	return redirect(url_for('admin.role_list'))


@admin.route('/user_list', methods=('GET', 'POST'))
@login_required
@admin_required
def user_list():
	"""
	用户列表
	:return:
	"""
	users = User.objects
	return render_template('admin/user_list.html', users=users)


@admin.route('/user_add/', methods=('GET', 'POST'))
@login_required
@admin_required
def user_add():
	"""
	添加用户
	:return:
	"""
	form = UserForm()
	roles = Role.objects
	return render_template('admin/user_add.html', form=form, roles=roles)


@admin.route('/user_save/', methods=('GET', 'POST'))
@login_required
@admin_required
def user_save():
	"""
	用户保存
	:return:
	"""
	user = User()
	username = request.form.get('username')
	password = request.form.get('password')
	role = request.form.get('role')
	if username:
		user.username = username
	if password:
		user.password = bcrypt.generate_password_hash(password)
	if role:
		user.role = int(role)
	user.save()
	return redirect(url_for('admin.user_list'))


@admin.route('/user_edit/<string:uid>/', methods=('GET', 'POST'))
@login_required
@admin_required
def user_edit(uid):
	"""
	编辑用户
	:param rid:
	:return:
	"""
	user = User.objects(id=uid).first()
	roles = Role.objects
	form = UserForm()
	form.username.data = user.username
	return render_template('admin/user_edit.html', form=form, user=user, roles=roles)


@admin.route('/user_editsave/', methods=('GET', 'POST'))
@login_required
@admin_required
def user_editsave():
	"""
	保存用户编辑
	:return:
	"""
	uid = request.form.get('uid')
	user = User.objects(id=uid).first()
	username = request.form.get('username')
	password = request.form.get('password')
	role = request.form.get('role')
	if username:
		user.username = username
	if password:
		user.password = bcrypt.generate_password_hash(password)
	if role:
		user.role = int(role)
	user.save()
	return redirect(url_for('admin.user_list'))


@admin.route('/user_del/<string:uid>/', methods=('GET', 'POST'))
@login_required
@admin_required
def user_del(uid):
	"""
	删除用户
	:param uid:
	:return:
	"""
	user = None
	if uid:
		user = User.objects(id=uid).first()
	if not user:
		flash(u'对不起，角色不存在或已经删除')
	else:
		user.delete()
		flash(u'删除角色成功')
	return redirect(url_for('admin.user_list'))
