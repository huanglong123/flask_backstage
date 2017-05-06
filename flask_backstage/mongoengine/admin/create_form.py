# -*- coding:utf-8 -*-
from flask_mongoengine.wtf import orm
from wtforms import fields as f, validators
from .widgets import DateTimePickerField


class CustomModelConverter(orm.ModelConverter):
	def __init__(self, view):
		super(CustomModelConverter, self).__init__()

		self.view = view

	def _get_field_override(self, name):
		form_overrides = getattr(self.view, 'form_overrides', None)

		if form_overrides:
			return form_overrides.get(name)

		return None

	def convert(self, model, field, field_args):
		kwargs = {
			'label': getattr(field, 'verbose_name', field.name),
			'description': getattr(field, 'help_text', None) or '',
			'validators': getattr(field, 'validators', None) or [],
			'filters': getattr(field, 'filters', None) or [],
			'default': field.default,
		}
		if field_args:
			kwargs.update(field_args)

		if kwargs['validators']:
			# Create a copy of the list since we will be modifying it.
			kwargs['validators'] = list(kwargs['validators'])

		if field.required:
			kwargs['validators'].append(validators.InputRequired())
		else:
			kwargs['validators'].append(validators.Optional())

		ftype = type(field).__name__

		if field.choices:
			kwargs['choices'] = field.choices

			if ftype in self.converters:
				kwargs["coerce"] = self.coerce(ftype)
			multiple_field = kwargs.pop('multiple', False)
			radio_field = kwargs.pop('radio', False)
			if multiple_field:
				return f.SelectMultipleField(**kwargs)
			if radio_field:
				return f.RadioField(**kwargs)
			return f.SelectField(**kwargs)

		ftype = type(field).__name__

		if hasattr(field, 'to_form_field'):
			return field.to_form_field(model, kwargs)

		override = self._get_field_override(field.name)
		if override:
			return override(**kwargs)

		if ftype in self.converters:
			return self.converters[ftype](model, field, kwargs)

	@orm.converts('DateTimeField')
	def conv_DateTime(self, model, field, kwargs):
		return DateTimePickerField(**kwargs)
