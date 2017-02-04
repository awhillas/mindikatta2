from __future__ import unicode_literals

from django.db import models


class Farm(models.Model):
	id = models.CharField(max_length=2, primary_key=True)
	name = models.CharField(max_length=15)
	address = models.CharField(max_length=255)


class SalesDocket(models.Model):
	docket_number = models.CharField(max_length=10)
	date = models.DateField()
	delivery_weight = models.IntegerField()
	percent_moisture = models.DecimalField(max_digits=3, decimal_places=1)
	premium_weight = models.IntegerField()
	commercial_weight = models.IntegerField()
	oil_weight = models.IntegerField()
	net_payment = models.DecimalField(max_digits=8, decimal_places=2)


class Silo(models.Model):
	name = models.CharField(max_length=10)
	capacity = models.IntegerField()
	export = models.BooleanField()


class Variety(models.Model):
	name = models.CharField(max_length=20)
	block = models.CharField(max_length=20)
	charting_colour = models.CharField(max_length=12)
	farm = models.ForeignKey(Farm)


class Weighings(models.Model):
	operation = models.CharField(max_length=6)
	to_silo = models.ForeignKey(Silo, related_name='+')
	from_silo = models.ForeignKey(Silo, related_name='+')
	silo_emptyed = models.BooleanField()
	variety = models.ForeignKey(Variety)
	weight = models.IntegerField()
	report_date = models.DateTimeField()
