# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-09 01:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('harvest', '0006_auto_20170209_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesdocket',
            name='commercial_weight',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='salesdocket',
            name='oil_weight',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='salesdocket',
            name='premium_weight',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterModelTable(
            name='salesdocket',
            table='harvest_sales_docket',
        ),
    ]