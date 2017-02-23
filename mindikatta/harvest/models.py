from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.humanize.templatetags.humanize import intcomma


class Farm(models.Model):  # same as Orchard
	id = models.CharField(max_length=2, primary_key=True)
	name = models.CharField(max_length=15)
	address = models.CharField(max_length=255)
	
	def __str__(self):
		return "{}".format(self.name)


class SalesDocket(models.Model):
	
	def __str__(self):
		return "{} ({})".format(self.consignment_number, self.delivery_date)

	# farm = models.ForeignKey(Farm, null=True)
	
	consignment_number = models.CharField(max_length=10)
	delivery_date = models.DateField(default=timezone.now)
	net_payment = models.DecimalField(max_digits=8, decimal_places=2, default=0) # --> ncv_total_value - mic35_pct_mc_total_levy
	# kg_weight_received = models.IntegerField()
	# moisture_content_pct = models.DecimalField(max_digits=3, decimal_places=1)
	
	# Map old names to new names...
	
	@property
	def docket_number(self):
		return self.consignment_number
		
	@property
	def delivery_weight(self):
		return self.kg_weight_received

	@property
	def percent_moisture(self):
		return self.moisture_content_pct

	# @property
	# def net_payment(self):
	# 	return self.ncv_total_value - self.mic35_pct_mc_total_levy
	
	@property
	def date(self):
		return self.delivery_date
	
	
	# Consignment XML imported data
	
	kg_weight_received = models.FloatField(help_text="KG-Weight_Received, ", blank=True, default=0.0)
	moisture_content_pct = models.FloatField(help_text="MoistureContent-pct, ", blank=True, default=0.0)
	kg_weight10_pct_mc = models.FloatField(help_text="KG-Weight10%M.C., ", blank=True, default=0.0)
	foreign_matter_pct = models.FloatField(help_text="Foreign_matter%, ", blank=True, default=0.0)
	premium_kernel_recovery_pct = models.FloatField(help_text="Premium Kernel Recovery %, ", blank=True, default=0.0)
	total_commercial_kr_pct = models.FloatField(help_text="Total Commercial KR%, ", blank=True, default=0.0)
	light_discoloration_pct = models.FloatField(help_text="Light Discoloration %", blank=True, default=0.0)
	light_germination_pct = models.FloatField(help_text="Light Germination%", blank=True, default=0.0)
	light_immaturity_kr_pct = models.FloatField(help_text="Light Immaturity KR%", blank=True, default=0.0)
	reject_penalty_cost_aud = models.FloatField(help_text="Reject Penalty Cost AUD", blank=True, default=0.0)
	total_reject_pct = models.FloatField(help_text="Total Reject%, Reject Kernel Recovery", blank=True, default=0.0)
	heavy_discoloration_pct = models.FloatField(help_text="Heavy Discoloration%, Reject Kernel Recovery", blank=True, default=0.0)
	heavy_germination_pct = models.FloatField(help_text="Heavy Germination %, Reject Kernel Recovery", blank=True, default=0.0)
	heavy_immaturity_pct = models.FloatField(help_text="Heavy Immaturity%, Reject Kernel Recovery", blank=True, default=0.0)
	insect_damage_pct = models.FloatField(help_text="Insect Damage%, Reject Kernel Recovery", blank=True, default=0.0)
	internal_discolouration_pct = models.FloatField(help_text="Internal Discolouration%, Reject Kernel Recovery", blank=True, default=0.0)
	mould_units_pct = models.FloatField(help_text="Mould Units%, Reject Kernel Recovery", blank=True, default=0.0)
	total_kernel_recovery_pct = models.FloatField(help_text="Total Kernel Recovery%", blank=True, default=0.0)
	shell_units_pct = models.FloatField(help_text="Shell Units%", blank=True, default=0.0)
	total_units_pct = models.FloatField(help_text="Total units=%", blank=True, default=0.0)
	ncv_premium_nis_per_kg_nis = models.FloatField(help_text="NCV Premium NIS /Kg NIS, Notional Consignment Value", blank=True, default=0.0)
	ncv_commercial_nis_per_kg_nis = models.FloatField(help_text="NCV Commercial NIS /Kg NIS, Notional Consignment Value", blank=True, default=0.0)
	ncv_whole_kernel_pct = models.FloatField(help_text="NCV Whole Kernel %, Notional Consignment Value", blank=True, default=0.0)
	ncv_whole_kernel_adjustmnt_pct = models.FloatField(help_text="NCV Whole Kernel Adjustmnt %, Notional Consignment Value", blank=True, default=0.0)
	ncv_reject_adjustment_per_kg_nis = models.FloatField(help_text="NCV Reject adjustment /Kg NIS, Notional Consignment Value", blank=True, default=0.0)
	ncv_freight_subsidy_per_kg = models.FloatField(help_text="NCV Freight Subsidy/Kg, Notional Consignment Value", blank=True, default=0.0)
	ncv_total_per_kg_nis = models.FloatField(help_text="NCV Total /Kg NIS, Notional Consignment Value", blank=True, default=0.0)
	ncv_total_value = models.FloatField(help_text="NCV Total Value, Notional Consignment Value", blank=True, default=0.0)
	mic35_pct_mc_premium_kernel_pct = models.FloatField(help_text="MIC3.5%MC Prem.Kernel %, Macadamia Industry Calculation", blank=True, default=0.0)
	mic35_pct_mc_premium_kernel_kg = models.FloatField(help_text="MIC3.5%MC Prem.Kernel Kg, Macadamia Industry Calculation", blank=True, default=0.0)
	mic35_pct_mc_commercial_kernel_pct = models.FloatField(help_text="MIC3.5%MC Com.Kernel %, Macadamia Industry Calculation", blank=True, default=0.0)
	mic35_pct_mc_commercial_kernel_kg = models.FloatField(help_text="MIC3.5%MC Com.Kernel Kg, Macadamia Industry Calculation", blank=True, default=0.0)
	mic35_pct_mc_reject_kernel_pct = models.FloatField(help_text="MIC3.5%MC Rej.Kernel %, Macadamia Industry Calculation", blank=True, default=0.0)
	mic35_pct_mc_reject_kernel_kg = models.FloatField(help_text="MIC3.5%MC Rej.Kernel Kg, Macadamia Industry Calculation", blank=True, default=0.0)
	mic35_pct_mc_total_kernel_pct = models.FloatField(help_text="MIC3.5%MC Tot.Kernel %, Macadamia Industry Calculation", blank=True, default=0.0)
	total_pct_leviable_kernel = models.FloatField(help_text="Total% Leviable Kernel, Macadamia Industry Calculation", blank=True, default=0.0)
	mic35_pct_mc_total_kernel_kg = models.FloatField(help_text="MIC3.5%MC Total Kernel Kg, Macadamia Industry Calculation", blank=True, default=0.0)
	mic35_pct_mc_levy_per_kg = models.FloatField(help_text="MIC3.5%MC Levy /Kg, Macadamia Industry Calculation", blank=True, default=0.0)
	mic35_pct_mc_total_levy = models.FloatField(help_text="MIC3.5%MC Total Levy, Macadamia Industry Calculation", blank=True, default=0.0)
	first_payment_value = models.FloatField(help_text="First Payment Value, Payment Particulars", blank=True, default=0.0)
	compulsory_levy = models.FloatField(help_text="Compulsory Levy, Payment Particulars", blank=True, default=0.0)
	laboratory_fee = models.FloatField(help_text="Laboratory Fee, Payment Particulars", blank=True, default=0.0)
	payment_due = models.FloatField(help_text="Payment due, Payment Particulars", blank=True, default=0.0)
	ni_st_ytd = models.FloatField(help_text="NIS(t) YTD, YTD & Last 3 Years data", blank=True, default=0.0)
	pkr_pct_ytd = models.FloatField(help_text="PKR% YTD, YTD & Last 3 Years data", blank=True, default=0.0)
	ckr_pct_ytd = models.FloatField(help_text="CKR% YTD, YTD & Last 3 Years data", blank=True, default=0.0)
	rkr_pct_ytd = models.FloatField(help_text="RKR% YTD, YTD & Last 3 Years data", blank=True, default=0.0)
	wk_pct_ytd = models.FloatField(help_text="WK% YTD, YTD & Last 3 Years data", blank=True, default=0.0)
	ni_st_1_year_prev = models.FloatField(help_text="NIS(t) 1 Yr Prev, YTD & Last 3 Years data", blank=True, default=0.0)
	pkr_pct_1_year_prev = models.FloatField(help_text="PKR% 1 Yr Prev, YTD & Last 3 Years data", blank=True, default=0.0)
	ckr_pct_1_year_prev = models.FloatField(help_text="CKR% 1 Yr Prev, YTD & Last 3 Years data", blank=True, default=0.0)
	rkr_pct_1_year_prev = models.FloatField(help_text="RKR% 1 Yr Prev, YTD & Last 3 Years data", blank=True, default=0.0)
	wk_pct_1_year_prev = models.FloatField(help_text="WK% 1 Yr Prev, YTD & Last 3 Years data", blank=True, default=0.0)
	ni_st_2_year_prev = models.FloatField(help_text="NIS(t) 2 Yr Prev, YTD & Last 3 Years data", blank=True, default=0.0)
	pkr_pct_2_year_prev = models.FloatField(help_text="PKR% 2 Yr Prev, YTD & Last 3 Years data", blank=True, default=0.0)
	ckr_pct_2_year_prev = models.FloatField(help_text="CKR% 2 Yr Prev, YTD & Last 3 Years data", blank=True, default=0.0)
	rkr_pct_2_year_prev = models.FloatField(help_text="RKR% 2 Yr Prev, YTD & Last 3 Years data", blank=True, default=0.0)
	wk_pct_2_year_prev = models.FloatField(help_text="WK% 2 Yr Prev, YTD & Last 3 Years data", blank=True, default=0.0)
	ni_st_3_year_prev = models.FloatField(help_text="NIS(t) 3 Yr Prev, YTD & Last 3 Years data", blank=True, default=0.0)
	pkr_pct_3_year_prev = models.FloatField(help_text="PKR% 3 Yr Prev, YTD & Last 3 Years data", blank=True, default=0.0)
	ckr_pct_3_year_prev = models.FloatField(help_text="CKR% 3 Yr Prev, YTD & Last 3 Years data", blank=True, default=0.0)
	rkr_pct_3_year_prev = models.FloatField(help_text="RKR% 3 Yr Prev, YTD & Last 3 Years data", blank=True, default=0.0)
	wk_pct_3_year_prev = models.FloatField(help_text="WK% 3 Yr Prev, YTD & Last 3 Years data", blank=True, default=0.0)


class Silo(models.Model):
	name = models.CharField(max_length=10)
	capacity = models.IntegerField()
	export = models.IntegerField(default=0)
	
	def __str__(self):
		return "{}".format(self.name)


class Block(models.Model):
	name = models.CharField(max_length=20)
	charting_colour = models.CharField(max_length=12)
	farm = models.ForeignKey(Farm)

	def __str__(self):
		return "{}, {}".format(self.name, self.farm)
		
	class Meta:
		verbose_name = "Block"
		verbose_name_plural = "Blocks"


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
	block = models.ForeignKey(Block)
	weight = models.IntegerField()
	report_date = models.DateTimeField(default=timezone.now)

	class Meta:
		verbose_name = "Weighing"
		verbose_name_plural = "Weighings"

	def __str__(self):
		return "{}, ({}) {}".format(self.operation, self.weight, self.block)
