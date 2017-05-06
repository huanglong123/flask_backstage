# -*- coding:utf-8 -*-
from flask_wtf import FlaskForm
from flask import request
from flask_login import current_user
from collections import Iterable


def expose(url='/', methods=('GET',)):
    """动态生成路由"""

    def wrap(f):
        if not hasattr(f, '_urls'):
            f._urls = []
        f._urls.append((url, methods))
        return f

    return wrap


def get_field_value(model, name):
    """获取model对应字段的值"""
    return getattr(model, name)


def is_form_submitted():
    return request and request.method in ('PUT', 'POST')


class MyForm(FlaskForm):
    """重写populate_obj方法"""

    def populate_obj(self, obj):
        for name, field in self._fields.items():
            if request.form.get(name) is None or request.form.get(name) is '':
                continue
            field.populate_obj(obj, name)


def get_form(model, converter, field_args, base_class=MyForm):
    """返回一个表单类"""
    properties = sorted(((k, v) for k, v in model._fields.items()), key=lambda v: v[1].creation_counter)  # 对字典进行排序
    field_dict = {}
    for name, p in properties:
        field = converter.convert(model, p, field_args)  # 调用convert方法，返回对应的field
        if field is not None:
            field_dict[name] = field
    field_dict['model_class'] = model
    return type(model.__name__ + 'Form', (base_class,), field_dict)  # 构造表单类


def cadmin_create_required(role=None):
    """
    cadmin权限装饰器
    :param role: 角色值
    :return:
    """

    if not isinstance(current_user.role, int):
        raise Exception('role参数必须是整数')
    if isinstance(role, int):
        if current_user.role >= role:
            return True
        else:
            return False
    if isinstance(role, Iterable):
        if current_user.role in role:
            return True
        else:
            return False
