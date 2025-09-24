from django.urls import path
from .views import(
    BusinessUnitListAPIView,
    BusinessUnitCreateAPIView,
    CalendarYearListAPIView,
    CalendarYearCreateAPIView,
)

urlpatterns = [
    path('unit/', BusinessUnitListAPIView.as_view(), name='business-unit-list'),
    path('unit/create/', BusinessUnitCreateAPIView.as_view(), name='business-unit-create'),
    path('calendar-year/', CalendarYearListAPIView.as_view(), name='calendar-year-list'),
    path('calendar-year/create/', CalendarYearCreateAPIView.as_view(), name='calendar-year-create'),
]
    