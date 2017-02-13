from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.humanize.templatetags.humanize import intcomma


class Farm(models.Model):
	id = models.CharField(max_length=2, primary_key=True)
	name = models.CharField(max_length=15)
	address = models.CharField(max_length=255)
	
	def __str__(self):
		return "{}".format(self.name)


class SalesDocket(models.Model):
	docket_number = models.CharField(max_length=10)
	date = models.DateField(default=timezone.now)
	delivery_weight = models.IntegerField()
	percent_moisture = models.DecimalField(max_digits=3, decimal_places=1)
	net_payment = models.DecimalField(max_digits=8, decimal_places=2)
	# premium_weight = models.IntegerField(default=0)
	# commercial_weight = models.IntegerField(default=0)
	# oil_weight = models.IntegerField(default=0)
	
	def __str__(self):
		return "{} ({})".format(self.docket_number, self.date)
	


class Silo(models.Model):
	name = models.CharField(max_length=10)
	capacity = models.IntegerField()
	export = models.IntegerField(default=0)
	
	def __str__(self):
		return "{}".format(self.name)


class Variety(models.Model):
	name = models.CharField(max_length=20)
	block = models.CharField(max_length=20)
	charting_colour = models.CharField(max_length=12)
	farm = models.ForeignKey(Farm)

	def __str__(self):
		return "{}, {}".format(self.name, self.block)


class Weighings(models.Model):
	OP_CHOICES = (
		('dehusk', 'Dehusk'),
		('resort', 'Resort'),
		('sale', 'Sale'),
	)
	operation = models.CharField(max_length=6, choices=OP_CHOICES, default='dehusk')
	to_silo = models.ForeignKey(Silo, related_name='+')
	from_silo = models.ForeignKey(Silo, related_name='+')
	# silo_emptyed = models.IntegerField(default=0)
	variety = models.ForeignKey(Variety)
	weight = models.IntegerField()
	report_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return "{}, ({})".format(self.weight, self.variety, self.operation)
