from django.urls import path
from .views import(
    JournalEntryCreateAPIView,
    CashDisbursementCreateAPIView,
)

urlpatterns = [
    path('journal-entry/', JournalEntryCreateAPIView.as_view(), name='journal-line-list'),
    path('cash-disbursement/create/', CashDisbursementCreateAPIView.as_view(), name='cash-disbursement-create'),
]