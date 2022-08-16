import html5.forms.widgets as html5
from crispy_forms.bootstrap import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from django import forms
from django.conf import settings
from django.forms import widgets
from django.utils.dateparse import parse_datetime
from django.utils.encoding import force_str

from .models import SalesDocket, Silo, Weighings


class CommonLayout(Layout):
    def __init__(self, *args, **kwargs):
        super(CommonLayout, self).__init__(
            "weight",
            "block",
            InlineRadios("operation", css_class="btn-group"),
            Div(
                Div("from_silo", css_class="col-sm-6"),
                Div("to_silo", css_class="col-sm-6"),
                css_class="row",
            ),
            "report_date",
            FormActions(Submit("save", "Save"), Button("cancel", "Cancel")),
        )


class WeighingsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.html5_required = True  # HTML5 required attribute.
        self.helper.layout = CommonLayout()

    class Meta:
        model = Weighings
        fields = ["operation", "to_silo", "from_silo", "block", "weight", "report_date"]
        widgets = {
            "report_date": html5.DateInput(),
            # 'from_silo': widgets.RadioSelect(),
            # 'to_silo': widgets.RadioSelect(),
            # 'block': widgets.RadioSelect(),
        }

    def clean_weight(self):
        if self.cleaned_data["weight"] < 0:
            raise forms.ValidationError("Must be greater then zero")
        return self.cleaned_data["weight"]

    def clean(self):
        # Check to_silo and from_silo are not the same
        if self.data["to_silo"] == self.data["from_silo"]:
            raise forms.ValidationError("To and From silos can not be the same")
        return self.cleaned_data


class CounterForm(WeighingsForm):
    counter = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.helper = FormHelper()
        # self.helper.html5_required = True # HTML5 required attribute.
        self.helper.form_action = "harvest:weighing"
        self.helper.layout = Layout(
            Fieldset("Report Weighing Coutner", "counter", CommonLayout())
        )
        self.fields["weight"].initial = -69  # so the form submits. see: clean_weight()

    class Meta(WeighingsForm.Meta):
        WeighingsForm.Meta.widgets["weight"] = widgets.HiddenInput()

    def clean_counter(self):
        if int(self.data["counter"]) < 0:
            raise forms.ValidationError("Must be greater then zero")

    def clean_weight(self):
        return int(self.data["counter"]) * settings.HARVEST_WEIGHT_PER_COUNT


class ISODateTimeField(forms.DateTimeField):
    def strptime(self, value, format):
        return parse_datetime(force_str(value))


class SalesDocketForm(forms.ModelForm):
    # delivery_date = ISODateTimeField() # ???

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.html5_required = True  # HTML5 required attribute.

        # TODO: clean this up.
        self.helper.layout = Layout(
            "docket_number",
            "consignment_number",
            "kg_weight_received",
            "delivery_date",
            "block",
            "moisture_content_pct",
            "kg_weight10_pct_mc",
            "ncv_total_value",
            "net_payment",
            "total_levy",
            "total_leviable_kernel",
            "dehusking_sorting",
            FormActions(Submit("save", "Save changes"), Button("cancel", "Cancel")),
        )

    class Meta:
        model = SalesDocket
        fields = "__all__"
        widgets = {
            "delivery_date": html5.DateInput(),
        }

    def clean_net_payment(self):
        if int(self.cleaned_data["net_payment"]) < 0:
            raise forms.ValidationError("Must be greater then zero")
        return self.cleaned_data["net_payment"]

    def clean_moisture_content_pct(self):
        value = float(self.cleaned_data["moisture_content_pct"])
        if value < 0.0 and value > 100.0:
            raise forms.ValidationError("Must be greater then zero and less that 100")
        return self.cleaned_data["moisture_content_pct"]

    def clean_kg_weight_received(self):
        if int(self.cleaned_data["kg_weight_received"]) < 0:
            raise forms.ValidationError("Must be greater then zero")
        return self.cleaned_data["kg_weight_received"]
