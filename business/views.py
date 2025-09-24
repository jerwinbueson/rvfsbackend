from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView
from .models import(
    BusinessUnit,
    CalendarYear,
)
from .serializers import(
    BusinessUnitSerializer,
    CalendarYearSerializer,
)


class BusinessUnitListAPIView(ListAPIView):
    queryset = BusinessUnit.objects.all()
    serializer_class = BusinessUnitSerializer
    

class BusinessUnitCreateAPIView(CreateAPIView):
    queryset = BusinessUnit.objects.all()
    serializer_class = BusinessUnitSerializer

class CalendarYearListAPIView(ListAPIView):
    queryset = CalendarYear.objects.all()
    serializer_class = CalendarYearSerializer

class CalendarYearCreateAPIView(CreateAPIView):
    queryset = CalendarYear.objects.all()
    serializer_class = CalendarYearSerializer