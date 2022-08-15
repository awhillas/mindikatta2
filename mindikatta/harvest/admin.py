# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Block, Farm, SalesDocket, Silo, Weighings


class FarmAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "address")
    search_fields = ("name",)


admin.site.register(Farm, FarmAdmin)


class SalesDocketAdmin(admin.ModelAdmin):
    list_display = (
        "delivery_date",
        "consignment_number",
        "docket_number",
        "block",
        "net_payment",
        "kg_weight_received",
        "moisture_content_pct",
        "kg_weight10_pct_mc",
        "ncv_total_value",
        "total_levy",
        "total_leviable_kernel",
        "dehusking_sorting",
    )
    list_filter = ("delivery_date",)


admin.site.register(SalesDocket, SalesDocketAdmin)


class SiloAdmin(admin.ModelAdmin):
    list_display = ("name", "capacity", "export")
    search_fields = ("name",)


admin.site.register(Silo, SiloAdmin)


class BlockAdmin(admin.ModelAdmin):
    list_display = ("name", "farm")
    list_filter = ("farm",)
    search_fields = ("name",)


admin.site.register(Block, BlockAdmin)


class WeighingsAdmin(admin.ModelAdmin):
    list_display = (
        "report_date",
        "operation",
        "to_silo",
        "from_silo",
        "block",
        "weight",
    )
    list_filter = ("report_date",)
    raw_id_fields = ("to_silo", "from_silo", "block")


admin.site.register(Weighings, WeighingsAdmin)
