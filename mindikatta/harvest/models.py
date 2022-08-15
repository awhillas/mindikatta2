from __future__ import unicode_literals

from django.contrib.humanize.templatetags.humanize import intcomma
from django.db import models
from django.utils import timezone


class Farm(models.Model):  # same as Orchard
    id = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=15)
    address = models.CharField(max_length=255)

    def __str__(self):
        return "{}".format(self.name)


class Silo(models.Model):
    name = models.CharField(max_length=10)
    capacity = models.IntegerField()
    export = models.IntegerField(default=0)

    def __str__(self):
        return "{}".format(self.name)


class Block(models.Model):
    # Variety really...
    name = models.CharField(max_length=20)
    charting_colour = models.CharField(max_length=12)
    farm = models.ForeignKey(Farm, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{}, {}".format(self.name, self.farm)

    class Meta:
        verbose_name = "Block"
        verbose_name_plural = "Blocks"


class Weighings(models.Model):
    OP_CHOICES = (
        ("dehusk", "Dehusk"),
        ("resort", "Resort"),
        ("sale", "Sale"),
    )
    operation = models.CharField(max_length=6, choices=OP_CHOICES, default="dehusk")
    to_silo = models.ForeignKey(
        Silo, related_name="+", null=True, blank=True, on_delete=models.DO_NOTHING
    )
    from_silo = models.ForeignKey(
        Silo, related_name="+", null=True, blank=True, on_delete=models.DO_NOTHING
    )
    # silo_emptyed = models.IntegerField(default=0)
    block = models.ForeignKey(Block, on_delete=models.DO_NOTHING)
    weight = models.IntegerField()
    report_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Weighing"
        verbose_name_plural = "Weighings"
        permissions = (
            ("view_weighings_reports", "View Weighing Report Summaries"),
            ("download_weighings_data", "Download Weighing CSV data"),
        )

    def __str__(self):
        return "{}, ({}) {}".format(self.operation, self.weight, self.block)


class SalesDocket(models.Model):
    class Meta:
        verbose_name = "Consignment"
        verbose_name_plural = "Consignments"
        permissions = (
            ("view_salesdocket_reports", "View Consignments Report Summaries"),
            ("download_salesdocket_data", "Download Consignments CSV data"),
        )

    def __str__(self):
        return "{} ({})".format(self.consignment_number, self.delivery_date)

    # farm = models.ForeignKey(Farm, null=True)

    # These are the original fields that actually got populated

    consignment_number = models.CharField(max_length=10)
    delivery_date = models.DateField(default=timezone.now)
    kg_weight_received = models.FloatField(
        help_text="Delivery Weight", blank=True, default=0.0
    )
    moisture_content_pct = models.FloatField(
        help_text="MoistureContent-%, ", blank=True, default=0.0
    )
    net_payment = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    # These are new as of 2022

    docket_number = models.CharField(
        max_length=10, default=0, help_text="Delivery Docket No."
    )
    block = models.ForeignKey(Block, on_delete=models.DO_NOTHING, null=True)
    kg_weight10_pct_mc = models.FloatField(
        blank=True, default=0.0, help_text="Weight at 10% Moisture Content, KG"
    )
    ncv_total_value = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        default=0,
        help_text="Total Consignment Value",
    )
    total_levy = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, default=0, help_text="Industry Levy"
    )
    total_leviable_kernel = models.FloatField(
        blank=True, default=0.0, help_text="Total leviable kernel, kg"
    )
    dehusking_sorting = models.FloatField(
        blank=True, default=0.0, help_text="Dehusking / Sorting"
    )

    # Map old names to new names...

    @property
    def delivery_weight(self):
        return self.kg_weight_received

    @property
    def percent_moisture(self):
        return self.moisture_content_pct

    @property
    def date(self):
        return self.delivery_date
