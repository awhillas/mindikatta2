from django.contrib.auth.models import Group, User
from rest_framework import serializers

from .models import Weighings


class WeighingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weighings
        fields = "__all__"
        depth = 1
