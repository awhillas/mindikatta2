import calendar
import csv
import datetime
from pprint import pprint

import inflection
import numpy as np
import pandas as pd
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Sum
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    TemplateView,
    UpdateView,
    View,
)

from . import forms, models

abbr_month_to_digit = dict((v.lower(), k) for k, v in enumerate(calendar.month_abbr))


def qs_to_df(qs):
    """QuerySet to DataFrame"""
    Model = qs.model
    np_array = np.core.records.fromrecords(
        qs.values_list(), names=[f.name for f in Model._meta.fields]
    )
    return pd.DataFrame(np_array)


def parse_consignment_xml(raw_xml):
    import xml.etree.ElementTree as et

    def clean(text):
        translate = {
            # 'PKR': 'Premium Kernel Recovery'
            # 'CKR': 'Commercial Kernel Recovery'
            # 'RKR': 'Reject Kernel Recovery'
            # 'KR': 'Kernel Recovery'
            "Yr": "Year",
            "No.": "number",
            "10%": "_10pct",
            "3.5%": "_35pct",
            "%MC": "_pct_moisture",
            "%": "_pct",
            "Rej.": "Reject ",
            "Prem.": "Premium ",
            "Com.": "Commercial ",
            "Tot.": "Total",
            "/Kg": "_per_kg",
            # 'YTD': 'year to Date'
        }
        for old, new in translate.items():
            text = text.replace(old, new)
        text = text.strip()
        text = text.translate(
            str.maketrans(
                {" ": "_", "%": "", ".": "", "(": "", ")": "", '"': "", "=": ""}
            )
        )
        text = text.replace("__", "_")
        return inflection.underscore(text)

    data = {}
    root = et.fromstring(raw_xml)

    data["consignment_number"] = root.find("Load-ID.").find("Consignment-No.").text

    dd = root.find("Delivery_Details")
    for data_point in ["DeliveryDate", "ReportDateTime"]:
        db_name = inflection.underscore(data_point)  # convert to snake_case
        data[db_name] = dd.find(data_point).text

    skip_list = ["QR-Date", "Dehusking-Sorting Charge/Kg"]
    for test in root.find("DeliveryTestResults").iter("Test"):
        name = test.find("TestName").text
        value = test.find("TestResult").text.strip()
        if name in skip_list:
            continue
        clean_name = clean(name)
        data[clean_name] = float(value)

    return data


def format_df(df, groupby_col):
    # Totals grouped by ...
    df_out = (
        df.groupby(
            [
                groupby_col,  # ...operation...
                df["report_date"].map(
                    lambda x: calendar.month_name[x.month]
                ),  # ...and month.
            ]
        )
        .sum()["weight"]
        .unstack()
        .fillna(0)
    )
    df_out["Total"] = df_out.sum(axis=1)
    return df_out


def get_latest_year():
    return int(
        models.Weighings.objects.all().order_by("report_date").last().report_date.year
    )


def get_available_years():
    return [d.year for d in models.Weighings.objects.dates("report_date", "year")]


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


class BaseTemplateView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy("login")


class Home(BaseTemplateView):
    template_name = "harvest/home.html"
    breadcrumbs = ["home"]

    def get_weighings(self, year):
        return models.Weighings.objects.filter(report_date__year=year)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["farms"] = models.Farm.objects.all()
        context["current_year"] = (
            get_latest_year() if "year" not in kwargs else kwargs["year"]
        )
        context["avaiable_years"] = get_available_years()
        context["avaiable_years"].reverse()

        # Get the last year we have data for
        qs = self.get_weighings(context["current_year"])
        df = qs_to_df(qs)

        context["operations"] = dict(models.Weighings.OP_CHOICES)
        context["blocks"] = {
            d["id"]: d["name"] for d in models.Block.objects.all().values("id", "name")
        }

        context["operations_summary"] = format_df(df, "operation")
        context["block_summary_dehusk"] = format_df(
            df[df["operation"] == "dehusk"], "block"
        )
        context["block_summary_resort"] = format_df(
            df[df["operation"] == "resort"], "block"
        )
        context["block_summary_sale"] = format_df(
            df[df["operation"] == "sale"], "block"
        )

        return context


class Reports(Home):
    # template_name = "harvest/reports.html"
    breadcrumbs = ["reports"]

    def get_weighings(self, year):
        blocks = models.Block.objects.filter(farm=self.kwargs["farm"])
        qs = models.Weighings.objects.filter(report_date__year=year)
        qs = qs.filter(block__in=blocks)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["farm_id"] = models.Farm.objects.get(pk=self.kwargs["farm"])
        return context


class WeighingInput(PermissionRequiredMixin, CreateView):
    permission_required = "harvest.add_weighings"
    model = models.Weighings
    form_class = forms.CounterForm  # Using the counter form not the weighings form
    template_name = "object_form.html"
    success_url = reverse_lazy("harvest:weighing_list")
    breadcrumbs = ["weightings"]


class WeighingEdit(WeighingInput, UpdateView):
    permission_required = "harvest.change_weighings"
    form_class = forms.WeighingsForm
    breadcrumbs = ["weightings"]


class WeighingRemove(PermissionRequiredMixin, DeleteView):
    permission_required = "harvest.delete_weighings"
    model = models.Weighings
    # template_name = "object_delete.html"
    success_url = reverse_lazy("harvest:weighing_list")
    breadcrumbs = ["weightings"]


class WeighingListing(PermissionRequiredMixin, ListView):
    permission_required = "harvest.add_weighings"
    model = models.Weighings
    ordering = "-report_date"
    breadcrumbs = ["weightings"]

    def get_queryset(self):
        qs = models.Weighings.objects.all()

        # filter params

        year = self.kwargs.get("year", False)
        if year:
            qs = qs.filter(report_date__year=year)
        else:
            qs = qs.filter(report_date__year=datetime.datetime.now().year)

        operation = self.kwargs.get("operation", False)
        if operation:
            qs = qs.filter(operation=operation)

        # GET params

        sort = self.request.GET.get("sort", False)
        if sort:
            qs = qs.order_by(sort)
        else:
            qs = qs.order_by("-report_date")

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sort"] = self.request.GET.get("sort", False)
        context["avaiable_years"] = get_available_years()
        context["avaiable_years"].reverse()
        context["current_op"] = self.kwargs.get("operation", "")
        context["current_year"] = int(
            self.kwargs.get("year", datetime.datetime.now().year)
        )
        return context


class WeighingBreakdown(PermissionRequiredMixin, ListView):
    permission_required = "harvest.view_weighings_reports"
    breadcrumbs = ["weightings"]
    template_name = "harvest/breakdown.html"
    farm = False
    year = datetime.datetime.now().year
    month = ""
    operation = "dehusk"

    def get_queryset(self):
        qs = models.Weighings.objects.all()

        # filter params
        self.farm = farm = self.kwargs.get("farm", False)
        if farm:
            blocks = models.Block.objects.filter(farm=farm)
            qs = qs.filter(block__in=blocks)

        self.month = month = self.kwargs.get(
            "month", calendar.month_abbr[datetime.datetime.now().month].lower()
        )
        if month:
            qs = qs.filter(report_date__month=abbr_month_to_digit[month.lower()])

        self.year = year = self.kwargs.get("year", datetime.datetime.now().year)
        qs = qs.filter(report_date__year=year)

        self.operation = operation = self.kwargs.get("operation", False)
        if operation:
            qs = qs.filter(operation=operation)

        self.block = block = self.kwargs.get("block", False)
        if block:
            qs = qs.filter(block=block)

        # GET params

        sort = self.request.GET.get("sort", "-report_date")
        qs = qs.order_by(sort)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["months"] = abbr_month_to_digit
        context["total"] = self.get_queryset().aggregate(Sum("weight"))["weight__sum"]
        context["farm_name"] = (
            models.Farm.objects.get(id=self.farm).name if self.farm else False
        )
        context["month_display"] = calendar.month_name[abbr_month_to_digit[self.month]]
        return context


class SalesDocketInput(PermissionRequiredMixin, CreateView):
    permission_required = "harvest.add_salesdocket"
    model = models.SalesDocket
    form_class = forms.SalesDocketForm
    template_name = "object_form.html"
    success_url = reverse_lazy("harvest:sales_list")
    breadcrumbs = ["sales"]

    def form_invalid(self, form):
        return super().form_invalid(form)

    def form_valid(self, form):
        return super().form_valid(form)


class SalesDocketEdit(PermissionRequiredMixin, UpdateView):
    permission_required = "harvest.change_salesdocket"
    model = models.SalesDocket
    form_class = forms.SalesDocketForm
    template_name = "object_form.html"
    success_url = reverse_lazy("harvest:sales_list")
    breadcrumbs = ["sales"]


class SalesDocketRemove(PermissionRequiredMixin, DeleteView):
    permission_required = "harvest.delete_salesdocket"
    model = models.SalesDocket
    # template_name = 'object_form.html'
    success_url = reverse_lazy("harvest:sales_list")
    breadcrumbs = ["sales"]


class SalesDocketListing(PermissionRequiredMixin, ListView):
    permission_required = "harvest.add_salesdocket"
    model = models.SalesDocket
    ordering = "-delivery_date"
    breadcrumbs = ["sales"]

    def get_queryset(self):
        qs = models.SalesDocket.objects.all()

        # filter params

        year = self.kwargs.get("year", False)
        if year:
            qs = qs.filter(delivery_date__year=year)
        else:
            qs = qs.filter(delivery_date__year=datetime.datetime.now().year)

        # GET params
        sort = self.request.GET.get("sort", False)
        if sort:
            qs = qs.order_by(sort)
        else:
            qs = qs.order_by("-delivery_date")

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sort"] = self.request.GET.get("sort", False)
        context["avaiable_years"] = [
            d.year for d in models.SalesDocket.objects.dates("delivery_date", "year")
        ]
        context["avaiable_years"].reverse()
        context["current_year"] = int(
            self.kwargs.get("year", datetime.datetime.now().year)
        )
        return context


class CSVResponseMixin(object):
    """
    A mixin that can be used to render a CSV response.
    """

    def render_to_csv_response(self, context, **response_kwargs):
        """
        Returns a CSV response, transforming 'context' to make the payload.
        """
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="somefilename.csv"'

        qs = self.get_queryset()

        writer = csv.writer(response)
        headers = [f.name for f in qs.first()._meta.get_fields()]
        writer.writerow(headers)  # header row
        for row in qs:
            d = model_to_dict(row)
            writer.writerow([d[key] for key in headers])

        return response

    def get_data(self, context):
        """
        Returns an object that will be serialized as CSV by json.dumps().
        """
        return context


class WeighingListingCSV(CSVResponseMixin, WeighingListing):
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_csv_response(context, **response_kwargs)


class ProcessConsignment(LoginRequiredMixin, TemplateView):
    template_name = "harvest/upload_consignment.html"

    def post(self, request, *args, **kwargs):
        # process the XML
        data = parse_consignment_xml(
            request.body.decode("utf-8").encode("ascii", "ignore")
        )
        data["net_payment"] = data["ncv_total_value"] - data["compulsory_levy"]
        form = forms.SalesDocketForm(data)
        if form.is_valid():
            new_salesdocket = form.save()
            return JsonResponse(
                {
                    "result": "ok",
                    "redirect_url": reverse(
                        "harvest:sale_edit", args=[new_salesdocket.pk]
                    ),
                }
            )
        else:
            pprint(form.errors)
            return HttpResponse(status=400)
