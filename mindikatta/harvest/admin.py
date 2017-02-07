# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Farm, SalesDocket, Silo, Variety, Weighings


class FarmAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'address')
	search_fields = ('name',)
admin.site.register(Farm, FarmAdmin)


class SalesDocketAdmin(admin.ModelAdmin):
	list_display = (
		'docket_number',
		'date',
		'delivery_weight',
		'percent_moisture',
		'net_payment',
	)
	list_filter = ('date',)
admin.site.register(SalesDocket, SalesDocketAdmin)


class SiloAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'capacity', 'export')
	list_filter = ('export',)
	search_fields = ('name',)
admin.site.register(Silo, SiloAdmin)


class VarietyAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'block', 'charting_colour', 'farm')
	list_filter = ('farm',)
	search_fields = ('name',)
admin.site.register(Variety, VarietyAdmin)


class WeighingsAdmin(admin.ModelAdmin):
	list_display = (
		'report_date',
		'operation',
		'variety',
		'weight',
		# 'silo_emptyed',
		'to_silo',
		'from_silo',
	)
	list_filter = ('report_date',)
	raw_id_fields = ('to_silo', 'from_silo', 'variety')
admin.site.register(Weighings, WeighingsAdmin)
