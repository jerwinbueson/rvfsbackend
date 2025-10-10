from django.urls import path
from .views import(
    JournalEntryCreateAPIView,

)

urlpatterns = [
    path('journal-entry/', JournalEntryCreateAPIView.as_view(), name='journal-line-list'),
]