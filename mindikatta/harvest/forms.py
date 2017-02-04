from django import forms
from harvest.models import Weighings, SalesDocket


class WeighingsForm(forms.Form):
    operation = forms.CharField(label='Operation', max_length=6)
    to_silo = forms.ModelChoiceField(label='To silo')
    from_silo = forms.ModelChoiceField(label='From silo')
    silo_emptyed = forms.BooleanField(label='Silo emptyed', required=False)
    variety = forms.ModelChoiceField(label='Variety')
    weight = forms.IntegerField(label='Weight')
    report_date = forms.DateTimeField(label='Report date')


class SalesDocketForm(forms.Form):
    docket_number = forms.CharField(label='Docket number', max_length=10)
    date = forms.DateField(label='Date')
    delivery_weight = forms.IntegerField(label='Delivery weight')
    percent_moisture = forms.DecimalField(label='Percent moisture', max_digits=3, decimal_places=1)
    premium_weight = forms.IntegerField(label='Premium weight')
    commercial_weight = forms.IntegerField(label='Commercial weight')
    oil_weight = forms.IntegerField(label='Oil weight')
    net_payment = forms.DecimalField(label='Net payment', max_digits=8, decimal_places=2)
