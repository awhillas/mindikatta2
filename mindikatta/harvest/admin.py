# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Block, Farm, SalesDocket, Silo, Weighings


class FarmAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "address")
    search_fields = ("name",)


admin.site.register(Farm, FarmAdmin)


class SalesDocketAdmin(admin.ModelAdmin):
    list_display = (
        "consignment_number",
        "delivery_date",
        "net_payment",
        "kg_weight_received",
        "moisture_content_pct",
        "kg_weight10_pct_mc",
        "foreign_matter_pct",
        "premium_kernel_recovery_pct",
        "total_commercial_kr_pct",
        "light_discoloration_pct",
        "light_germination_pct",
        "light_immaturity_kr_pct",
        "reject_penalty_cost_aud",
        "total_reject_pct",
        "heavy_discoloration_pct",
        "heavy_germination_pct",
        "heavy_immaturity_pct",
        "insect_damage_pct",
        "internal_discolouration_pct",
        "mould_units_pct",
        "total_kernel_recovery_pct",
        "shell_units_pct",
        "total_units_pct",
        "ncv_premium_nis_per_kg_nis",
        "ncv_commercial_nis_per_kg_nis",
        "ncv_whole_kernel_pct",
        "ncv_whole_kernel_adjustmnt_pct",
        "ncv_reject_adjustment_per_kg_nis",
        "ncv_freight_subsidy_per_kg",
        "ncv_total_per_kg_nis",
        "ncv_total_value",
        "mic35_pct_mc_premium_kernel_pct",
        "mic35_pct_mc_premium_kernel_kg",
        "mic35_pct_mc_commercial_kernel_pct",
        "mic35_pct_mc_commercial_kernel_kg",
        "mic35_pct_mc_reject_kernel_pct",
        "mic35_pct_mc_reject_kernel_kg",
        "mic35_pct_mc_total_kernel_pct",
        "total_pct_leviable_kernel",
        "mic35_pct_mc_total_kernel_kg",
        "mic35_pct_mc_levy_per_kg",
        "mic35_pct_mc_total_levy",
        "first_payment_value",
        "compulsory_levy",
        "laboratory_fee",
        "payment_due",
        "ni_st_ytd",
        "pkr_pct_ytd",
        "ckr_pct_ytd",
        "rkr_pct_ytd",
        "wk_pct_ytd",
        "ni_st_1_year_prev",
        "pkr_pct_1_year_prev",
        "ckr_pct_1_year_prev",
        "rkr_pct_1_year_prev",
        "wk_pct_1_year_prev",
        "ni_st_2_year_prev",
        "pkr_pct_2_year_prev",
        "ckr_pct_2_year_prev",
        "rkr_pct_2_year_prev",
        "wk_pct_2_year_prev",
        "ni_st_3_year_prev",
        "pkr_pct_3_year_prev",
        "ckr_pct_3_year_prev",
        "rkr_pct_3_year_prev",
        "wk_pct_3_year_prev",
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
