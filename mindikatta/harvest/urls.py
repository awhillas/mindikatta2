"""mindikatta URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from . import views

app_name = "harvest"

urlpatterns = [
	url(r'^$', views.Home.as_view(), name='home'),
	url(r'^reports/$', views.Reports.as_view(), name='reports'),

	# Weighings

	url(r'^weighing/$', views.WeighingInput.as_view(), name='weighing'),
	url(r'^weighing/(?P<pk>[0-9]+)/$', views.WeighingEdit.as_view(), name='weighing_edit'),
	url(r'^weighing/(?P<pk>[0-9]+)/delete$', views.WeighingRemove.as_view(), name='weighing_delete'),
	
	url(r'^weighings/$', views.WeighingListing.as_view(), name='weighing_list'),
	url(r'^weighings/(?P<year>[0-9]{4})/$', views.WeighingListing.as_view(), name='weighing_list'),
	url(r'^weighings/(?P<year>[0-9]{4})/(?P<operation>(dehusk|resort|sale))/$', views.WeighingListing.as_view(), name='weighing_list'),
	# CSV versions
	url(r'^weighings/(?P<year>[0-9]{4})/csv/$', views.WeighingListingCSV.as_view(), name='weighing_list_csv'),
	url(r'^weighings/(?P<year>[0-9]{4})/(?P<operation>(dehusk|resort|sale))/csv/$', views.WeighingListingCSV.as_view(), name='weighing_list_csv'),

	url(r'^docket/$', views.SalesDocketInput.as_view(), name='sales'),
	url(r'^docket/(?P<pk>[0-9]+)/$', views.SalesDocketEdit.as_view(), name='sale_edit'),
	url(r'^docket/(?P<pk>[0-9]+)/delete$', views.SalesDocketRemove.as_view(), name='sale_delete'),
	url(r'^sales/$', views.SalesDocketListing.as_view(), name='sales_list'),
	url(r'^sales/(?P<year>[0-9]{4})/$', views.SalesDocketListing.as_view(), name='sales_list'),
]
