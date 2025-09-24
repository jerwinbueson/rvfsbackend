from rest_framework import serializers
from .models import(
    BusinessUnit,
    CalendarYear,
)

class BusinessUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessUnit
        fields = '__all__'


class CalendarYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarYear
        fields = '__all__'