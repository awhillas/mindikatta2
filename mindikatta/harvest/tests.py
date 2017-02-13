from pprint import pprint

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

from . import forms


class HarvestViewsTest(TestCase):
	def setUp(self):
		User = get_user_model()
		self.scout_user = User.objects.create_user(username='tester', password='tester123')

	def test_reports_views_redirects_strangers(self):
		""" Test reports view redirects if not logged in """
		response = self.client.get(reverse('harvest:reports'))
		self.assertEqual(response.status_code, 302)

	def test_home_views_redirects_strangers(self):
		""" Test home view redirects if not logged in """
		response = self.client.get(reverse('harvest:home'))
		self.assertEqual(response.status_code, 302)  # if not logged in

	def test_reports_views_works(self):
		""" Test reports view works if logged in """
		self.assertTrue(self.client.login(username='tester', password='tester123'))  # login
		response = self.client.get(reverse('harvest:reports'))
		self.assertEqual(response.status_code, 200)

	def test_home_views_works(self):
		""" Test home view works if logged in """
		self.assertTrue(self.client.login(username='tester', password='tester123'))  # login
		response = self.client.get(reverse('harvest:home'))
		self.assertEqual(response.status_code, 200)  # if not logged in


class HarvestFormTests(TestCase):
	fixtures = ["mindikatta/harvest/fixtures/"+f for f in ["farm.json", "silo.json", "variety.json"]]

	def test_WeighingsForm(self):
		""" WeighingsForm with valid data """
		form_data = {
			'operation': 'dehusk',
			'to_silo': 1,
			'from_silo': 2,
			'variety': 1,
			'weight': 1234,
			'report_date': '1/6/1969'
		}
		form = forms.WeighingsForm(data=form_data)
		self.assertTrue(form.is_valid())

	def test_CounterForm(self):
		""" CounterForm with valid data """
		form_data = {
			'counter': 10,
			'operation': 'dehusk',
			'to_silo': 1,
			'from_silo': 2,
			'variety': 1,
			'weight': -1,  # calculated from 'counter'
			'report_date': '1/6/1969'
		}
		form = forms.CounterForm(data=form_data)
		# pprint(form.errors)
		self.assertTrue(form.is_valid())

	def test_SalesDocketForm(self):
		""" SalesDocketForm with valid data """
		form_data = {
			'docket_number': 1234,
			'date': '1/6/1969',
			'delivery_weight': 69,
			'percent_moisture': 69.4,
			'net_payment': 666
		}
		form = forms.SalesDocketForm(data=form_data)
		# pprint(form.errors)
		self.assertTrue(form.is_valid())


# class HarvestCRUDViewTests(TestCase):
# 	def
