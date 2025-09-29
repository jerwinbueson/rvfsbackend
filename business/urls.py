from django.urls import path
from .views import(
    BusinessUnitListAPIView,
    BusinessUnitCreateAPIView,
    CalendarYearListAPIView,
    CalendarYearCreateAPIView,
    CurrentCalendarYear,
    UserBusinessUnit,
)

urlpatterns = [
    path('unit/', BusinessUnitListAPIView.as_view(), name='business-unit-list'),
    path('unit/create/', BusinessUnitCreateAPIView.as_view(), name='business-unit-create'),
    path('calendar-year/', CalendarYearListAPIView.as_view(), name='calendar-year-list'),
    path('calendar-year/create/', CalendarYearCreateAPIView.as_view(), name='calendar-year-create'),
    path('calendar-year/current/', CurrentCalendarYear.as_view(), name='current-calendar-year'),
    path('user-business/', UserBusinessUnit.as_view(), name='user-business'),
]
    