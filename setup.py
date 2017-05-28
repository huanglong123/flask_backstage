#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name='flask_backstage',
      version='0.2.1',
      description='A backstage framework with very few code.',
      author='pengwei',
      author_email='1300896173@qq.com',
      url='https://github.com/huanglong123/flask-backstage',
      packages=find_packages(),
      include_package_data=True,
      license='MIT',
      platforms='any',
      install_requires=[
          'Flask>=0.7',
          'Flask-WTF',
          'Flask-Bcrypt',
          'Flask-Login',
          'flask-mongoengine',
          'Flask-WTF'
      ],
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   'Programming Language :: Python :: 3.5',
                   ],
      )
