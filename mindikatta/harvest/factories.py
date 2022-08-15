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

    consignment_number = factory.fuzzy.FuzzyText(length=9)
    delivery_date = factory.Faker("date_time", tzinfo=pytz.timezone("Europe/Paris"))
    kg_weight_received = factory.fuzzy.FuzzyFloat(10.0)
    moisture_content_pct = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    net_payment = factory.fuzzy.FuzzyFloat(0.0, 1.0)
    docket_number = factory.fuzzy.FuzzyInteger(666, 100000)
    block = factory.Iterator(models.Block.objects.all())
    kg_weight10_pct_mc = factory.fuzzy.FuzzyFloat(0.1, 0.99)
    ncv_total_value = factory.fuzzy.FuzzyFloat(0.0, 10000.0)
    total_levy = factory.fuzzy.FuzzyFloat(0.0, 100.0)
    total_leviable_kernel = factory.fuzzy.FuzzyFloat(0.0, 100.0)
    dehusking_sorting = factory.fuzzy.FuzzyFloat(0.0, 100.0)
