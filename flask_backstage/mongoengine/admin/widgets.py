# -*- coding:utf-8 -*-
from wtforms import widgets, fields


class DateTimePickerWidget(widgets.TextInput):
	data_role = 'datatime'

	def __call__(self, field, **kwargs):
		return super(DateTimePickerWidget, self).__call__(field, **kwargs)


class DateTimePickerField(fields.StringField):
	widget = DateTimePickerWidget()
