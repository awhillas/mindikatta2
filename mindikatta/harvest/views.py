from pprint import pprint
import datetime
import csv
import pandas as pd
import numpy as np
import calendar

import inflection
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, reverse
from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.forms.models import model_to_dict

from . import models, forms


def qs_to_df(qs):
	""" QuerySet to DataFrame """
	Model = qs.model
	np_array = np.core.records.fromrecords(qs.values_list(), names=[f.name for f in Model._meta.fields])
	return pd.DataFrame(np_array)


def parse_consignment_xml(raw_xml):
	import xml.etree.ElementTree as et
	
	def clean(text):
		translate = {
			# 'PKR': 'Premium Kernel Recovery'
			# 'CKR': 'Commercial Kernel Recovery'
			# 'RKR': 'Reject Kernel Recovery'
			# 'KR': 'Kernel Recovery'
			'Yr': 'Year',
			'No.': 'number',
			'10%': '_10pct',
			'3.5%': '_35pct',
			'%MC': '_pct_moisture',
			'%': '_pct',
			'Rej.': 'Reject ',
			'Prem.': 'Premium ',
			'Com.': 'Commercial ',
			'Tot.': 'Total',
			'/Kg': '_per_kg',
			# 'YTD': 'year to Date'
		}
		for old, new in translate.items():
			text = text.replace(old, new)
		text = text.strip()
		text = text.translate(str.maketrans({' ':'_','%':'', '.':'', '(':'', ')':'', '"':'', '=':''}))
		text = text.replace('__', '_')
		return inflection.underscore(text)
	
	data = {}
	root = et.fromstring(raw_xml)
	
	data['consignment_number'] = root.find('Load-ID.').find('Consignment-No.').text
	
	dd = root.find('Delivery_Details')
	for data_point in ['DeliveryDate', 'ReportDateTime']:
		db_name = inflection.underscore(data_point)  # convert to snake_case
		data[db_name] = dd.find(data_point).text
	
	skip_list = ['QR-Date', 'Dehusking-Sorting Charge/Kg']
	for test in root.find('DeliveryTestResults').iter('Test'):
		name = test.find('TestName').text
		value = test.find('TestResult').text.strip()
		if name in skip_list:
			continue
		clean_name = clean(name)
		data[clean_name] = float(value)
		
	return data


class BaseTemplateView(LoginRequiredMixin, TemplateView):
	login_url = reverse_lazy('login')


class Home(BaseTemplateView):
	template_name = "harvest/home.html"
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		# Get the last year we have data for
		
		context['latest_year'] = latest_year = int(models.Weighings.objects.all().order_by('report_date').last().report_date.year)
		
		# build a query of just that year
		
		qs = models.Weighings.objects.filter(report_date__year=latest_year)
		df = qs_to_df(qs)
		
		# Totals grouped by operation and month
		
		context['summary'] = df.groupby([
			'operation',
			df['report_date'].map(lambda x: x.month)
		]).sum()['weight'].unstack().to_dict()
		context['months'] = context['summary'].keys()
		context['month_names'] = [calendar.month_name[i] for i in context['months']]
		context['operations'] = dict(models.Weighings.OP_CHOICES)
		
		return context


class Reports(BaseTemplateView):
	template_name = "harvest/reports.html"


class WeighingInput(LoginRequiredMixin, CreateView):
	model = models.Weighings
	form_class = forms.CounterForm  # Using the counter form not the weighings form
	template_name = 'object_form.html'
	success_url = reverse_lazy('harvest:weighing_list')


class WeighingEdit(WeighingInput, UpdateView):
	form_class = forms.WeighingsForm


class WeighingRemove(LoginRequiredMixin, DeleteView):
	model = models.Weighings
	# template_name = "object_delete.html"
	success_url = reverse_lazy('harvest:weighing_list')


class WeighingListing(LoginRequiredMixin, ListView):
	model = models.Weighings
	ordering = '-report_date'

	def get_queryset(self):
		qs = models.Weighings.objects.all()
		
		# filter params
		
		year = self.kwargs.get('year', False)
		if year:
			qs = qs.filter(report_date__year = year)
		else:
			qs = qs.filter(report_date__year = datetime.datetime.now().year)

		operation = self.kwargs.get('operation', False)
		# print("operation", operation)
		if operation:
			qs = qs.filter(operation = operation)
		
		# GET params
		sort = self.request.GET.get('sort', False)
		if sort:
			qs = qs.order_by(sort)
		else:
			qs = qs.order_by('-report_date')
		
		return qs
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['sort'] = self.request.GET.get('sort', False)
		context['avaiable_years'] = [d.year for d in models.Weighings.objects.dates('report_date', 'year')]
		context['avaiable_years'].reverse()
		context['current_op'] = self.kwargs.get('operation', '')
		context['current_year'] = int(self.kwargs.get('year', datetime.datetime.now().year))
		return context


class SalesDocketInput(LoginRequiredMixin, CreateView):
	model = models.SalesDocket
	form_class = forms.SalesDocketForm
	template_name = 'object_form.html'
	success_url = reverse_lazy('harvest:sales_list')
	
	def form_invalid(self, form):
		# pprint(form.errors)
		return super().form_invalid(form)
	
	def form_valid(self, form):
		# pprint(form.cleaned_data)
		return super().form_valid(form)


class SalesDocketEdit(LoginRequiredMixin, UpdateView):
	model = models.SalesDocket
	form_class = forms.SalesDocketForm
	template_name = 'object_form.html'
	success_url = reverse_lazy('harvest:sales_list')


class SalesDocketRemove(LoginRequiredMixin, DeleteView):
	model = models.SalesDocket
	# template_name = 'object_form.html'
	success_url = reverse_lazy('harvest:sales_list')


class SalesDocketListing(LoginRequiredMixin, ListView):
	model = models.SalesDocket
	ordering = '-delivery_date'

	def get_queryset(self):
		qs = models.SalesDocket.objects.all()
		
		# filter params
		
		year = self.kwargs.get('year', False)
		# print("year", year)
		if year:
			qs = qs.filter(delivery_date__year = year)
		else:
			qs = qs.filter(delivery_date__year = datetime.datetime.now().year)
		
		# GET params
		sort = self.request.GET.get('sort', False)
		if sort:
			qs = qs.order_by(sort)
		else:
			qs = qs.order_by('-delivery_date')
		
		return qs

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['sort'] = self.request.GET.get('sort', False)
		context['avaiable_years'] = [d.year for d in models.SalesDocket.objects.dates('delivery_date', 'year')]
		context['avaiable_years'].reverse()
		context['current_year'] = int(self.kwargs.get('year', datetime.datetime.now().year))
		return context


class CSVResponseMixin(object):
	"""
	A mixin that can be used to render a CSV response.
	"""
	def render_to_csv_response(self, context, **response_kwargs):
		"""
		Returns a CSV response, transforming 'context' to make the payload.
		"""
		# Create the HttpResponse object with the appropriate CSV header.
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

		qs = self.get_queryset()

		writer = csv.writer(response)
		headers = [f.name for f in qs.first()._meta.get_fields()]
		writer.writerow(headers)  # header row
		for row in qs:
			d = model_to_dict(row)
			writer.writerow([d[key] for key in headers])

		return response
		
	def get_data(self, context):
		"""
		Returns an object that will be serialized as CSV by json.dumps().
		"""
		return context


class WeighingListingCSV(CSVResponseMixin, WeighingListing):
	def render_to_response(self, context, **response_kwargs):
		return self.render_to_csv_response(context, **response_kwargs)
	

class ProcessConsignment(LoginRequiredMixin, TemplateView):
	template_name = 'harvest/upload_consignment.html'
	
	def post(self, request, *args, **kwargs):
		# process the XML
		data = parse_consignment_xml(request.body.decode("utf-8").encode("ascii","ignore"))
		data['net_payment'] = data['ncv_total_value'] - data['compulsory_levy']
		form = forms.SalesDocketForm(data)
		if form.is_valid():
			new_salesdocket = form.save()
			return JsonResponse({ 'result': 'ok', 'redirect_url': reverse('harvest:sale_edit', args=[new_salesdocket.pk])})
		else:
			pprint(form.errors)
			return HttpResponse(status=400)
