from pprint import pprint
import datetime
import csv
import pandas as pd
import numpy as np
import calendar

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
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
	form_class = forms.CounterForm
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
		print("operation", operation)
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
		pprint(form.errors)
		return super().form_invalid(form)
	
	def form_valid(self, form):
		pprint(form.cleaned_data)
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
	ordering = '-date'

	def get_queryset(self):
		qs = models.SalesDocket.objects.all()
		
		# filter params
		
		year = self.kwargs.get('year', False)
		print("year", year)
		if year:
			qs = qs.filter(date__year = year)
		else:
			qs = qs.filter(date__year = datetime.datetime.now().year)
		
		# GET params
		sort = self.request.GET.get('sort', False)
		if sort:
			qs = qs.order_by(sort)
		else:
			qs = qs.order_by('-date')
		
		return qs

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['sort'] = self.request.GET.get('sort', False)
		context['avaiable_years'] = [d.year for d in models.SalesDocket.objects.dates('date', 'year')]
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
