Flask_Backstage
===============

Flask_Backstage是一个基于flask的后台管理开发框架，能帮助你使用很少的时间和代码量开发出功能完备的管理后台。

Introduction
------------

Flask_Backstage 是基于flask的后台管理系统，采用了简洁强大的flask作为web框架，模板引擎用的是Jinja2，数据库用mongodb，前端AdminLTE框架。

依赖

Flask
Flask-Bcrypt
Flask-Login
flask-mongoengine
Flask-WTF

特性

内置用户管理，菜单管理，角色管理系统

提供类似的Flask Admin的BaseView,BaseModelView,帮助用户快速的开发增删改功能

Installation
------------
你可以通过pip快速安装Flask_Backstage扩展::

    pip install flask-backstage


Examples
--------
这里有个简单的项目使用案例，你也可以在这个项目的基础上编写自己的项目：https://github.com/huanglong123/flask_backstage_example

在线演示地址：http://backstage.kbiaoqing.cn/admin/

账号：admin  密码：123456


Documentation
-------------
简单的使用此项目, 你仅仅需要以下的几行代码::

    from flask import Flask
    from flask_backstage import Admin

    app = Flask(__name__)


    admin = Admin(app)

    app.run()


然后访问 http://127.0.0.1:5000/admin/
账号：admin
密码：123456



