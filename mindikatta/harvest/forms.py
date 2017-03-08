from django import forms
from django.conf import settings
from django.forms import widgets
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *
import html5.forms.widgets as html5
from django.utils.dateparse import parse_datetime
from django.utils.encoding import force_str

from .models import Weighings, SalesDocket, Silo


class CommonLayout(Layout):
	def __init__(self, *args, **kwargs):
		super(CommonLayout, self).__init__(
			'weight',
			'block',
			InlineRadios('operation', css_class="btn-group"),
			Div(
				Div('from_silo', css_class='col-sm-6'),
				Div('to_silo', css_class='col-sm-6'),
				css_class="row"
			),
			'report_date',
			FormActions(
				Submit('save', 'Save'),
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
		fields = ['operation', 'to_silo', 'from_silo', 'block', 'weight', 'report_date']
		widgets = {
			'report_date': html5.DateInput(),
			# 'from_silo': widgets.RadioSelect(),
			# 'to_silo': widgets.RadioSelect(),
			# 'block': widgets.RadioSelect(),
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
		# self.helper = FormHelper()
		# self.helper.html5_required = True # HTML5 required attribute.
		self.helper.form_action = 'harvest:weighing'
		self.helper.layout = Layout(
			Fieldset("Report Weighing Coutner",
				'counter',
				CommonLayout()
			)
		)
		self.fields['weight'].initial = -69
		
	class Meta(WeighingsForm.Meta):
		WeighingsForm.Meta.widgets['weight'] = widgets.HiddenInput()
		
	def clean_counter(self):
		if int(self.data['counter']) < 0:
			raise forms.ValidationError("Must be greater then zero")

	def clean_weight(self):
		return int(self.data['counter']) * settings.HARVEST_WEIGHT_PER_COUNT


class ISODateTimeField(forms.DateTimeField):
	def strptime(self, value, format):
		return parse_datetime(force_str(value))


class SalesDocketForm(forms.ModelForm):
	delivery_date = ISODateTimeField()
	report_date_time = ISODateTimeField()
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_tag = True
		self.helper.html5_required = True # HTML5 required attribute.
		
		# TODO: clean this up.
		self.helper.layout = Layout(
			'consignment_number', 'delivery_date', 'report_date_time', 'net_payment', 'kg_weight_received', 'moisture_content_pct', 'kg_weight10_pct_mc', 'foreign_matter_pct', 'premium_kernel_recovery_pct', 'total_commercial_kr_pct', 'light_discoloration_pct', 'light_germination_pct', 'light_immaturity_kr_pct', 'reject_penalty_cost_aud', 'total_reject_pct', 'heavy_discoloration_pct', 'heavy_germination_pct', 'heavy_immaturity_pct', 'insect_damage_pct', 'internal_discolouration_pct', 'mould_units_pct', 'total_kernel_recovery_pct', 'shell_units_pct', 'total_units_pct', 'ncv_premium_nis_per_kg_nis', 'ncv_commercial_nis_per_kg_nis', 'ncv_whole_kernel_pct', 'ncv_whole_kernel_adjustmnt_pct', 'ncv_reject_adjustment_per_kg_nis', 'ncv_freight_subsidy_per_kg', 'ncv_total_per_kg_nis', 'ncv_total_value', 'mic35_pct_mc_premium_kernel_pct', 'mic35_pct_mc_premium_kernel_kg', 'mic35_pct_mc_commercial_kernel_pct', 'mic35_pct_mc_commercial_kernel_kg', 'mic35_pct_mc_reject_kernel_pct', 'mic35_pct_mc_reject_kernel_kg', 'mic35_pct_mc_total_kernel_pct', 'total_pct_leviable_kernel', 'mic35_pct_mc_total_kernel_kg', 'mic35_pct_mc_levy_per_kg', 'mic35_pct_mc_total_levy', 'first_payment_value', 'compulsory_levy', 'laboratory_fee', 'payment_due', 'ni_st_ytd', 'pkr_pct_ytd', 'ckr_pct_ytd', 'rkr_pct_ytd', 'wk_pct_ytd', 'ni_st_1_year_prev', 'pkr_pct_1_year_prev', 'ckr_pct_1_year_prev', 'rkr_pct_1_year_prev', 'wk_pct_1_year_prev', 'ni_st_2_year_prev', 'pkr_pct_2_year_prev', 'ckr_pct_2_year_prev', 'rkr_pct_2_year_prev', 'wk_pct_2_year_prev', 'ni_st_3_year_prev', 'pkr_pct_3_year_prev', 'ckr_pct_3_year_prev', 'rkr_pct_3_year_prev', 'wk_pct_3_year_prev',
			FormActions(
				Submit('save', 'Save changes'),
				Button('cancel', 'Cancel')
			)
		)
		
		
	def clean_net_payment(self):
		if int(self.cleaned_data['net_payment']) < 0:
			raise forms.ValidationError("Must be greater then zero")
		return self.cleaned_data['net_payment']

	def clean_moisture_content_pct(self):
		value = float(self.cleaned_data['moisture_content_pct'])
		if value < 0.0 and value > 100.0:
			raise forms.ValidationError("Must be greater then zero and less that 100")
		return self.cleaned_data['moisture_content_pct']

	def clean_kg_weight_received(self):
		if int(self.cleaned_data['kg_weight_received']) < 0:
			raise forms.ValidationError("Must be greater then zero")
		return self.cleaned_data['kg_weight_received']
	
	class Meta:
		model = SalesDocket
		fields = '__all__'
		widgets = {
			'delivery_date': html5.DateInput(),
		}
