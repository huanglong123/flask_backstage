# -*- coding:utf-8 -*-

"""
网站权限相关的程序
"""

from functools import wraps
from flask import abort
from flask_login import current_user
from collections import Iterable

def admin_create_required(role=None):
    """
    admin权限装饰器
    :param role: 角色值
    :return:
    """
    if role is None:
        raise Exception('role参数是必填参数')

    def required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not isinstance(current_user.role, int):
                raise Exception('role参数必须是整数')
            if isinstance(role, int):
                if current_user.role >= role:
                    return f(*args, **kwargs)
                else:
                    abort(403)
            if isinstance(role, Iterable):
                if current_user.role in role:
                    return f(*args, **kwargs)
                else:
                    abort(403)
        return decorated_function
    return required