import os
from pprint import pprint

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from . import factories, forms, views


class HarvestGeneralViewsTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.scout_user = User.objects.create_superuser(
            username="tester",
            password="tester123",
            email="test@example.com",
            is_staff=True,
        )

    def test_reports_views_redirects_strangers(self):
        """Test reports view redirects if not logged in"""
        response = self.client.get(reverse("harvest:reports", args=["WW"]))
        self.assertEqual(response.status_code, 302)

    def test_home_views_redirects_strangers(self):
        """Test home view redirects if not logged in"""
        response = self.client.get(reverse("harvest:home"))
        self.assertEqual(response.status_code, 302)  # if not logged in

    def test_reports_views_works(self):
        """Test reports view works if logged in"""
        self.assertTrue(
            self.client.login(username="tester", password="tester123")
        )  # login
        response = self.client.get(reverse("harvest:reports", args=["WW"]))
        self.assertEqual(response.status_code, 200)

    def test_home_views_works(self):
        """Test home view works if logged in"""
        self.client.force_login(self.scout_user)  # login
        response = self.client.get(reverse("harvest:home"))
        self.assertEqual(response.status_code, 200)


class HarvestWeighingViewsTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.scout_user = User.objects.create_superuser(
            username="tester",
            password="tester123",
            email="test@example.com",
            is_staff=True,
        )
        self.scout_user.save()
        self.weighing = factories.WeighingsFactory.create()
        self.client.force_login(self.scout_user)  # login

    def test_create_weighing_view_works(self):
        """Test create 'weighing' view works"""
        view_name = "harvest:weighing"
        response = self.client.get(reverse(view_name))
        self.assertEqual(response.status_code, 200)  # OK

    # def test_create_weighing_form_submit_works(self):
    # 	view_name = 'harvest:weighing'
    # 	data = {
    # 		'operation': 'dehusk',
    # 		'to_silo': 0,
    # 		'from_silo': 1,
    # 		'block': 1,
    # 		'report_date': '01/06/1969',  # summer of '69 ;-)
    # 		'weight': -69,
    # 		'counter': 69
    # 	}
    # 	# Not logged in...
    # 	response = self.client.post(reverse(view_name), data)
    # 	self.assertEqual(response.status_code, 302)  # redirect to login
    # 	# After login...
    # 	# print(self.client.login(username='tester', password='tester123'))
    # 	self.client.force_login(self.scout_user)  # login
    # 	response = self.client.post(reverse(view_name), data, follow=True)
    # 	self.assertEqual(response.status_code, 200)  # and we're all good
    # 	self.assertTrue(len(response.redirect_chain) > 0)  # Should have been a redirect...
    # 	self.assertEqual(response.redirect_chain[0][0], reverse('harvest:weighing_list'))  # ...to weighing_list

    def test_weighing_edit_view_works(self):
        """Test 'weighing_edit' view works"""
        view_name = "harvest:weighing_edit"
        response = self.client.get(reverse(view_name, args=[self.weighing.pk]))
        self.assertEqual(response.status_code, 200)  # OK

    def test_weighing_delete_view_works(self):
        """Test 'weighing_edit' view works"""
        view_name = "harvest:weighing_delete"
        response = self.client.get(reverse(view_name, args=[self.weighing.pk]))
        self.assertEqual(response.status_code, 200)  # OK

    def test_weighing_listing_view_works(self):
        """Test weighing_list view works"""
        view_name = "harvest:weighing_list"
        response = self.client.get(reverse(view_name), follow=True)
        self.assertEqual(response.status_code, 200)  # OK
        # year filter
        response = self.client.get(reverse(view_name, args=["2016"]), follow=True)
        self.assertEqual(response.status_code, 200)  # OK

    def test_CSV_weighing_listing_view_works(self):
        """Test 'weighing_list_csv' view works"""
        view_name = "harvest:weighing_list_csv"
        response = self.client.get(reverse(view_name, args=["2016"]), follow=True)
        self.assertEqual(response.status_code, 200)  # OK

    def test_home_views_works(self):
        """Consignment view works"""
        response = self.client.get(reverse("harvest:home"))
        self.assertEqual(response.status_code, 200)  # if not logged in


class HarvestSalesDocketViewsTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.scout_user = User.objects.create_superuser(
            username="tester",
            password="tester123",
            email="test@example.com",
            is_staff=True,
        )
        self.salesdocket = factories.SalesDocketFactory.create()
        self.client.force_login(self.scout_user)  # login

    def test_create_salesdocket_view_works(self):
        """Test create 'sales' view works"""
        view_name = "harvest:sales"
        response = self.client.get(reverse(view_name), follow=True)
        self.assertEqual(response.status_code, 200)  # OK

    def test_salesdocket_edit_view_works(self):
        """Test 'sale_edit' view works"""
        view_name = "harvest:sale_edit"
        self.client.force_login(self.scout_user)  # login
        response = self.client.get(
            reverse(view_name, args=[self.salesdocket.pk]), follow=True
        )
        self.assertEqual(response.status_code, 200)  # OK

    def test_salesdocket_delete_view_works(self):
        """Test 'sale_delete' view works"""
        view_name = "harvest:sale_delete"
        self.client.force_login(self.scout_user)  # login
        response = self.client.get(
            reverse(view_name, args=[self.salesdocket.pk]), follow=True
        )
        self.assertEqual(response.status_code, 200)  # OK


class HarvestFormTests(TestCase):
    # fixtures = ["mindikatta/harvest/fixtures/"+f for f in ["farm.json", "silo.json", "block.json"]]

    def test_WeighingsForm(self):
        """WeighingsForm with valid data"""
        form_data = {
            "operation": "dehusk",
            "to_silo": 1,
            "from_silo": 2,
            "block": 1,
            "weight": 1234,
            "report_date": "1/6/1969",
        }
        form = forms.WeighingsForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_CounterForm(self):
        """CounterForm with valid data"""
        form_data = {
            "counter": 10,
            "operation": "dehusk",
            "to_silo": 1,
            "from_silo": 2,
            "block": 1,
            "weight": -1,  # calculated from 'counter'
            "report_date": "1/6/1969",
        }
        form = forms.CounterForm(data=form_data)
        # pprint(form.errors)
        self.assertTrue(form.is_valid())

    def test_SalesDocketForm(self):
        """SalesDocketForm with valid data"""
        form_data = {
            "consignment_number": 1234,
            "delivery_date": "2016-09-15T15:39:54",
            "report_date_time": "2016-09-15T15:39:54",  # this should not be required :-/
            "delivery_weight": 69,
            "moisture_content_pct": 69.4,
            "net_payment": 666.69,
            "kg_weight_received": 1234,
            "moisture_content_pct": 12.1,
        }
        form = forms.SalesDocketForm(data=form_data)
        # pprint(form.errors)
        self.assertTrue(form.is_valid())


class HarvestXMLParseTest(TestCase):
    def setUp(self):
        xml_file = os.path.join(settings.BASE_DIR, "data", "B3003_namera_cqrreport.xml")
        with open(xml_file, "r") as myfile:
            self.xml = myfile.read()

    def test_parse_consignment_xml(self):
        consignent = views.parse_consignment_xml(self.xml)


# class HarvestCRUDViewTests(TestCase):
# 	def setUp(self):
