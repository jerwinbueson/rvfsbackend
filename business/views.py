from accounts import serializers
from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission



from rest_framework import status
from .models import(
    BusinessUnit,
    CalendarYear,
)
from .serializers import(
    BusinessUnitSerializer,
    CalendarYearSerializer,
)
from django.shortcuts import get_object_or_404


class CurrentCalendarYear(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        year_id = request.session.get('calendar_year_id')

        if year_id:  # user already selected one
            calendar_year = get_object_or_404(CalendarYear, pk=year_id)
        else:
            # fall back to the default for the user's business unit
            # (replace with how you get the business_unit for the user)
            business_unit = request.user.company  # adjust to your model
            calendar_year = CalendarYear.objects.filter(
                business_unit=business_unit,
                default=True
            ).first()

            # optionally also save this in the session for later
            if calendar_year:
                request.session['calendar_year_id'] = calendar_year.id

        return Response(CalendarYearSerializer(calendar_year, context={'request': request}).data if calendar_year else None)

    def post(self, request):
        year_id = request.data.get('calendar_year_id')
        calendar_year = get_object_or_404(CalendarYear, pk=year_id)
        request.session['calendar_year_id'] = calendar_year.id
        request.session.modified = True
        return Response({'status': 'ok', 'calendar_year_id': calendar_year.id})


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

class UserBusinessUnit(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        business_unit = request.user.company
        serializer = BusinessUnitSerializer(business_unit)
        return Response(serializer.data)
    