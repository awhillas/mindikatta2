from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
import django_filters

from .serializers import WeighingSerializer
from .models import Weighings


class WeighingByYearFilter(django_filters.rest_framework.FilterSet):
	# see: https://django-filter.readthedocs.io/en/latest/guide/tips.html#common-problems-for-declared-filters
	year = django_filters.NumberFilter(name="report_date", lookup_expr='year')
	
	class Meta:
		model = Weighings
		fields = "__all__"


class WeighingViewSet(viewsets.ReadOnlyModelViewSet):
	"""
	API endpoint that allows Weighins to be viewed.
	"""
	queryset = Weighings.objects.all()
	serializer_class = WeighingSerializer
	permission_classes = [IsAdminUser]
	# see: http://www.django-rest-framework.org/api-guide/filtering/#djangofilterbackend
	filter_fields = ('operation')
	filter_class = WeighingByYearFilter
