# -*- coding:utf-8 -*-
"""
创建视图函数工具类
"""
from flask import Blueprint, request, render_template, redirect, url_for, abort
from .helps import expose, get_field_value, get_form, is_form_submitted
from .create_form import CustomModelConverter
from flask_login import login_required


class CAdmin(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app

    def add_view(self, view):
        """注册蓝图"""
        if self.app is not None:
            self.app.register_blueprint(view.create_blueprint())


class BaseView(object):
    """基础视图类:cvar create_blueprint方法返回生成的蓝图"""

    def __init__(self, endpoint=None, static_folder=None, template_folder=None, url_prefix=None):
        self.endpoint = endpoint
        self.static_folder = static_folder
        self.template_folder = template_folder
        self.url_prefix = url_prefix
        self._urls = []
        self.blueprint = None

        for p in dir(self):
            """给_urls赋值"""
            attr = getattr(self, p)

            if hasattr(attr, '_urls'):
                """有_urls的说明就是被expose注册的路由"""
                for url, methods in attr._urls:
                    self._urls.append((url, p, methods))

    def create_blueprint(self):
        if not self.endpoint:
            self.endpoint = self.__class__.__name__.lower()
        self.blueprint = Blueprint(self.endpoint, __name__, template_folder=self.template_folder, static_folder=self.static_folder, url_prefix=self.url_prefix)
        for url, name, methods in self._urls:
            """添加路由"""
            self.blueprint.add_url_rule(url, name, getattr(self, name), methods=methods)
        return self.blueprint


class BaseModelView(BaseView):
    """基础modelView"""
    column_labels = None  # 对应字段的标题显示，例子dict(title="标题", content="内容", time="发布时间", image='图片')
    name = None  #  所操作的model的名字，例子name='文章'，则前端显示的就是文章列表，添加文章，编辑文章这样的字样
    image_list = []  #  说明那个字段是图片，列表显示的时候就会以图片形式显示，而不是图片路径
    list_templates = 'admin/list.html'  # list模板路径
    create_templates = 'admin/create.html'  # create模板路径
    edit_templates = 'admin/edit.html'  #  edit模板路径
    can_create = True  #  控制是否有添加功能
    can_edit = True  #  控制是否有编辑功能
    can_delete = True  #  控制是否有删除功能

    def __init__(self, model, endpoint=None, static_folder=None, template_folder=None, url_prefix=None):
        self.model = model
        if not url_prefix:
            url_prefix = '/' + self.model.__name__.lower()
        super(BaseModelView, self).__init__(endpoint=endpoint, static_folder=static_folder, template_folder=template_folder, url_prefix=url_prefix)

    def _get_model_fields(self, model=None):
        """通过model获取model的字段名"""
        if model is None:
            model = self.model

        return sorted(model._fields.items(), key=lambda n: n[1].creation_counter)

    def scaffold_form(self):
        """调用get_form生成表单类"""
        form_class = get_form(self.model, CustomModelConverter(self), {})
        return form_class

    def create_form(self):
        return self.scaffold_form()

    @expose('/list/')
    @login_required
    def list_view(self):
        """列表"""
        if not self.is_accessible():
            abort(403)
        if not self.create_required():
            self.can_create = False
        if not self.edit_required():
            self.can_edit = False
        if not self.delete_required():
            self.can_delete = False
        fields = self._get_model_fields(self.model)
        page = request.args.get('page')  # 分页
        if not page:
            page = 1
        else:
            page = int(page)
        data = self.model.objects.paginate(page=page, per_page=10)
        return render_template(
            self.list_templates, data=data, name=self.name,
            fields=fields, get_field_value=get_field_value,
            column_labels=self.column_labels, url_prefix=self.url_prefix, image_list=self.image_list,
            can_create=self.can_create, can_edit=self.can_edit, can_delete=self.can_delete
        )

    @expose('/create/', methods=('GET', 'POST'))
    @login_required
    def create_view(self):
        """添加保存"""
        if not self.is_accessible():
            abort(403)
        if not self.create_required():
            abort(403)
        form = self.scaffold_form()()  # 调用scaffold_form生成表单类，并实例化这个表单
        if is_form_submitted():
            model = self.model()
            form.populate_obj(model)
            model.save()
            return redirect(url_for(".list_view"))
        return render_template(
            self.create_templates, name=self.name, form=form,
            column_labels=self.column_labels, create_url=url_for(".create_view"))

    @expose('/edit/', methods=('GET', 'POST'))
    @login_required
    def edit_view(self):
        """编辑保存"""
        if not self.is_accessible():
            abort(403)
        if not self.edit_required():
            abort(403)
        form = self.scaffold_form()()  # 调用scaffold_form生成表单类，并实例化这个表单
        if is_form_submitted():
            model_id = request.args.get('id')
            model = self.model.objects(id=model_id).first()
            form.populate_obj(model)
            model.save()
            return redirect(url_for(".list_view"))
        else:
            model_id = request.args.get('id')
            model = self.model.objects(id=model_id).first()
            form = self.scaffold_form()(obj=model)
            return render_template(
                self.edit_templates, name=self.name, form=form,
                column_labels=self.column_labels, edit_url=url_for(".edit_view"), id=model_id)

    @expose('/delete/')
    @login_required
    def delete_view(self):
        """删除"""
        if not self.is_accessible():
            abort(403)
        if not self.delete_required():
            abort(403)
        model_id = request.args.get('id')
        model = self.model.objects(id=model_id).first()
        model.delete()
        return redirect(url_for(".list_view"))

    def create_required(self):
        """
        添加操作的权限控制，通过重写这个函数达到对添加操作的权限控制
        :return:
        """
        return self.can_create

    def edit_required(self):
        """
        编辑操作的权限控制，通过重写这个函数达到对编辑操作的权限控制
        :return:
        """
        return self.can_edit

    def delete_required(self):
        """
        删除操作的权限控制，通过重写这个函数达到对删除操作的权限控制
        :return:
        """
        return self.can_delete

    def is_accessible(self):
        """
        所有操作的统一权限控制，通过重写这个函数达到对所有操作的权限控制
        :return:
        """
        return True
