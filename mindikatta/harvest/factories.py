import factory
import factory.fuzzy
import pytz

from . import models


class WeighingsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Weighings

    operation = "dehusk"  # factory.fuzzy.FuzzyChoice(models.Weighings.OP_CHOICES)
    from_silo = factory.Iterator(models.Silo.objects.all())
    # from and to silo can not be the same
    to_silo = factory.LazyAttribute(
        lambda o: models.Silo.objects.all().exclude(pk=o.from_silo.pk).first()
    )  # no work :(
    block = factory.Iterator(models.Block.objects.all())
    weight = factory.fuzzy.FuzzyInteger(10, 1000)
    report_date = factory.Faker("date_time", tzinfo=pytz.timezone("Europe/Paris"))


class SalesDocketFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.SalesDocket

    kg_weight_received = factory.fuzzy.FuzzyFloat(10.0)
    moisture_content_pct = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    kg_weight10_pct_mc = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    foreign_matter_pct = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    premium_kernel_recovery_pct = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    total_commercial_kr_pct = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    light_discoloration_pct = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    light_germination_pct = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    light_immaturity_kr_pct = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    reject_penalty_cost_aud = factory.fuzzy.FuzzyFloat(1.0, 1000.0)
    total_reject_pct = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    heavy_discoloration_pct = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    heavy_germination_pct = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    heavy_immaturity_pct = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    insect_damage_pct = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    internal_discolouration_pct = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    mould_units_pct = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    total_kernel_recovery_pct = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    shell_units_pct = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    total_units_pct = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    ncv_premium_nis_per_kg_nis = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    ncv_commercial_nis_per_kg_nis = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    ncv_whole_kernel_pct = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    ncv_whole_kernel_adjustmnt_pct = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    ncv_reject_adjustment_per_kg_nis = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    ncv_freight_subsidy_per_kg = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    ncv_total_per_kg_nis = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    ncv_total_value = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    mic35_pct_mc_premium_kernel_pct = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    mic35_pct_mc_premium_kernel_kg = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    mic35_pct_mc_commercial_kernel_pct = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    mic35_pct_mc_commercial_kernel_kg = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    mic35_pct_mc_reject_kernel_pct = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    mic35_pct_mc_reject_kernel_kg = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    mic35_pct_mc_total_kernel_pct = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    total_pct_leviable_kernel = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    mic35_pct_mc_total_kernel_kg = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    mic35_pct_mc_levy_per_kg = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    mic35_pct_mc_total_levy = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    first_payment_value = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    compulsory_levy = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    laboratory_fee = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    payment_due = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    ni_st_ytd = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    pkr_pct_ytd = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    ckr_pct_ytd = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    rkr_pct_ytd = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    wk_pct_ytd = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    ni_st_1_year_prev = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    pkr_pct_1_year_prev = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    ckr_pct_1_year_prev = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    rkr_pct_1_year_prev = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    wk_pct_1_year_prev = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    ni_st_2_year_prev = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    pkr_pct_2_year_prev = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    ckr_pct_2_year_prev = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    rkr_pct_2_year_prev = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    wk_pct_2_year_prev = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    ni_st_3_year_prev = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    pkr_pct_3_year_prev = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    ckr_pct_3_year_prev = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    rkr_pct_3_year_prev = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    wk_pct_3_year_prev = factory.fuzzy.FuzzyFloat(0.1, 0.99)
