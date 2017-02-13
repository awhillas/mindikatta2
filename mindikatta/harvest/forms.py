from django import forms
from django.conf import settings
from django.forms import widgets
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *
import html5.forms.widgets as html5

from .models import Weighings, SalesDocket, Silo


class CommonLayout(Layout):
	def __init__(self, *args, **kwargs):
		super(CommonLayout, self).__init__(
			'weight',
			'variety',
			InlineRadios('operation', css_class="btn-group"),
			Div(
				Div('from_silo', css_class='col-sm-6'),
				Div('to_silo', css_class='col-sm-6'),
				css_class="row"
			),
			'report_date',
			FormActions(
				Submit('save', 'Save changes'),
				Button('cancel', 'Cancel')
			)
		)


class WeighingsForm(forms.ModelForm):
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_tag = True
		self.helper.html5_required = True  # HTML5 required attribute.
		self.helper.layout = CommonLayout()
	
	class Meta:
		model = Weighings
		fields = ['operation', 'to_silo', 'from_silo', 'variety', 'weight', 'report_date']
		widgets = {
			'report_date': html5.DateInput(),
			# 'from_silo': widgets.RadioSelect(),
			# 'to_silo': widgets.RadioSelect(),
			# 'variety': widgets.RadioSelect(),
		}

	def clean_weight(self):
		if self.cleaned_data['weight'] < 0:
			raise forms.ValidationError("Must be greater then zero")
		return self.cleaned_data['weight']
	
	def clean(self):
		# Check to_silo and from_silo are not the same
		if self.data['to_silo'] == self.data['from_silo']:
			raise forms.ValidationError("To and From silos can not be the same")
		return self.cleaned_data


class CounterForm(WeighingsForm):
	counter = forms.IntegerField()
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.html5_required = True # HTML5 required attribute.
		self.helper.layout = Layout(
			'counter',
			Field('weight', type="hidden", value="666"),
			CommonLayout()
		)
		
	class Meta(WeighingsForm.Meta):
		WeighingsForm.Meta.widgets['weight'] = widgets.HiddenInput()
		
	def get_initial(self):
		return {
			'weight': -1
		}

	def clean_counter(self):
		if int(self.data['counter']) < 0:
			raise forms.ValidationError("Must be greater then zero")

	def clean_weight(self):
		return int(self.data['counter']) * settings.HARVEST_WEIGHT_PER_COUNT


class SalesDocketForm(forms.ModelForm):
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_tag = True
		self.helper.html5_required = True # HTML5 required attribute.
		self.helper.layout = Layout(
			'docket_number',
			AppendedText('delivery_weight', 'kg'),
			AppendedText('percent_moisture', '%'),
			PrependedText('net_payment', '$'),
			'date',
			FormActions(
				Submit('save', 'Save changes'),
				Button('cancel', 'Cancel')
			)
		)
		
	def clean_net_payment(self):
		if int(self.cleaned_data['net_payment']) < 0:
			raise forms.ValidationError("Must be greater then zero")
		return self.cleaned_data['net_payment']

	def clean_percent_moisture(self):
		value = float(self.cleaned_data['percent_moisture'])
		if value < 0.0 and value > 100.0:
			raise forms.ValidationError("Must be greater then zero and less that 100")
		return self.cleaned_data['percent_moisture']

	def clean_delivery_weight(self):
		if int(self.cleaned_data['delivery_weight']) < 0:
			raise forms.ValidationError("Must be greater then zero")
		return self.cleaned_data['delivery_weight']
	
	class Meta:
		model = SalesDocket
		fields = '__all__'
		widgets = {
			'date': html5.DateInput(),
		}
