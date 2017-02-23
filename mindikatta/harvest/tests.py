from pprint import pprint
import os

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.conf import settings

from . import forms, views, factories


class HarvestGeneralViewsTest(TestCase):
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
		self.assertEqual(response.status_code, 200)
		

class HarvestWeighingViewsTest(TestCase):
	def setUp(self):
		User = get_user_model()
		self.scout_user = User.objects.create_user(username='tester', password='tester123')
		self.weighing = factories.WeighingsFactory.create()

	def test_create_weighing_view_works(self):
		""" Test create 'weighing' view works """
		view_name = 'harvest:weighing'
		# Not logged in...
		response = self.client.get(reverse(view_name))
		self.assertEqual(response.status_code, 302)  # redirect to login
		# After login...
		self.assertTrue(self.client.login(username='tester', password='tester123'))  # login
		response = self.client.get(reverse(view_name))
		self.assertEqual(response.status_code, 200)  # OK

	def test_weighing_edit_view_works(self):
		""" Test 'weighing_edit' view works """
		view_name = 'harvest:weighing_edit'
		# Not logged in...
		response = self.client.get(reverse(view_name, args=[self.weighing.pk]))
		self.assertEqual(response.status_code, 302)  # redirect to login
		# After login...
		self.assertTrue(self.client.login(username='tester', password='tester123'))  # login
		response = self.client.get(reverse(view_name, args=[self.weighing.pk]))
		self.assertEqual(response.status_code, 200)  # OK

	def test_weighing_delete_view_works(self):
		""" Test 'weighing_edit' view works """
		view_name = 'harvest:weighing_delete'
		# Not logged in...
		response = self.client.get(reverse(view_name, args=[self.weighing.pk]))
		self.assertEqual(response.status_code, 302)  # redirect to login
		# After login...
		self.assertTrue(self.client.login(username='tester', password='tester123'))  # login
		response = self.client.get(reverse(view_name, args=[self.weighing.pk]))
		self.assertEqual(response.status_code, 200)  # OK

	def test_weighing_listing_view_works(self):
		""" Test weighing_list view works """
		view_name = 'harvest:weighing_list'
		# Not logged in...
		response = self.client.get(reverse(view_name))
		self.assertEqual(response.status_code, 302)  # redirect to login
		# After login...
		self.assertTrue(self.client.login(username='tester', password='tester123'))  # login
		response = self.client.get(reverse(view_name))
		self.assertEqual(response.status_code, 200)  # OK
		# year filter
		response = self.client.get(reverse(view_name, args=['2016']))
		self.assertEqual(response.status_code, 200)  # OK

	def test_CSV_weighing_listing_view_works(self):
		""" Test 'weighing_list_csv' view works """
		view_name = 'harvest:weighing_list_csv'
		# Not logged in...
		response = self.client.get(reverse(view_name, args=['2016']))
		self.assertEqual(response.status_code, 302)  # redirect to login
		# After login...
		self.assertTrue(self.client.login(username='tester', password='tester123'))  # login
		response = self.client.get(reverse(view_name, args=['2016']))
		self.assertEqual(response.status_code, 200)  # OK

	def test_home_views_works(self):
		""" Consignment view works """
		self.assertTrue(self.client.login(username='tester', password='tester123'))  # login
		response = self.client.get(reverse('harvest:home'))
		self.assertEqual(response.status_code, 200)  # if not logged in


class HarvestSalesDocketViewsTest(TestCase):
	def setUp(self):
		User = get_user_model()
		self.scout_user = User.objects.create_user(username='tester', password='tester123')
		self.salesdocket = factories.SalesDocketFactory.create()

	def test_create_salesdocket_view_works(self):
		""" Test create 'sales' view works """
		view_name = 'harvest:sales'
		# Not logged in...
		response = self.client.get(reverse(view_name))
		self.assertEqual(response.status_code, 302)  # redirect to login
		# After login...
		self.assertTrue(self.client.login(username='tester', password='tester123'))  # login
		response = self.client.get(reverse(view_name))
		self.assertEqual(response.status_code, 200)  # OK

	def test_salesdocket_edit_view_works(self):
		""" Test 'sale_edit' view works """
		view_name = 'harvest:sale_edit'
		# Not logged in...
		response = self.client.get(reverse(view_name, args=[self.salesdocket.pk]))
		self.assertEqual(response.status_code, 302)  # redirect to login
		# After login...
		self.assertTrue(self.client.login(username='tester', password='tester123'))  # login
		response = self.client.get(reverse(view_name, args=[self.salesdocket.pk]))
		self.assertEqual(response.status_code, 200)  # OK

	def test_salesdocket_delete_view_works(self):
		""" Test 'sale_delete' view works """
		view_name = 'harvest:sale_delete'
		# Not logged in...
		response = self.client.get(reverse(view_name, args=[self.salesdocket.pk]))
		self.assertEqual(response.status_code, 302)  # redirect to login
		# After login...
		self.assertTrue(self.client.login(username='tester', password='tester123'))  # login
		response = self.client.get(reverse(view_name, args=[self.salesdocket.pk]))
		self.assertEqual(response.status_code, 200)  # OK




class HarvestFormTests(TestCase):
	# fixtures = ["mindikatta/harvest/fixtures/"+f for f in ["farm.json", "silo.json", "block.json"]]

	def test_WeighingsForm(self):
		""" WeighingsForm with valid data """
		form_data = {
			'operation': 'dehusk',
			'to_silo': 1,
			'from_silo': 2,
			'block': 1,
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
			'block': 1,
			'weight': -1,  # calculated from 'counter'
			'report_date': '1/6/1969'
		}
		form = forms.CounterForm(data=form_data)
		# pprint(form.errors)
		self.assertTrue(form.is_valid())

	def test_SalesDocketForm(self):
		""" SalesDocketForm with valid data """
		form_data = {
			'consignment_number': 1234,
			'delivery_date': '1/6/1969',
			'delivery_weight': 69,
			'moisture_content_pct': 69.4,
			'net_payment': 666
		}
		form = forms.SalesDocketForm(data=form_data)
		# pprint(form.errors)
		self.assertTrue(form.is_valid())


class HarvestXMLParseTest(TestCase):
	def setUp(self):
		xml_file = os.path.join(settings.BASE_DIR,  'data', 'B3003_namera_cqrreport.xml')
		with open(xml_file, 'r') as myfile:
			self.xml = myfile.read()

	def test_parse_consignment_xml(self):
		consignent = views.parse_consignment_xml(self.xml)
		

# class HarvestCRUDViewTests(TestCase):
# 	def setUp(self):
