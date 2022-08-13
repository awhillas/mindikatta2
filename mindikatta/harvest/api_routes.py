from django.conf.urls import url
from rest_framework import routers

from . import api_views

# API routes

router = routers.DefaultRouter()
router.register(r"weighings", api_views.WeighingViewSet)

urlpatterns = [
    # url('^weighings/year/(?P<year>\d{4})/$', api_views.WeighingByYearViewSet.as_view),
]

urlpatterns += router.urls
