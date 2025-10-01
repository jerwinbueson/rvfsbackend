from django.urls import path
from .views import(
    JournalEntryListAPIView,
    JournalEntryCreateAPIView,
    JournalLineListAPIView,
    JournalLineCreateAPIView,
    CashReceiptListAPIView,
    CashReceiptCreateAPIView,
    CashDisbursementListAPIView,
    CashDisbursementCreateAPIView,
    SalesListAPIView,
    SalesCreateAPIView,
)

urlpatterns = [
    path('journal-entry/', JournalEntryListAPIView.as_view(), name='journal-entry-list'),
    path('journal-entry/create/', JournalEntryCreateAPIView.as_view(), name='journal-entry-create'),
    path('journal-line/', JournalLineListAPIView.as_view(), name='journal-line-list'),
    path('journal-line/create/', JournalLineCreateAPIView.as_view(), name='journal-line-create'),
    path('cash-receipt/', CashReceiptListAPIView.as_view(), name='cash-receipt-list'),
    path('cash-receipt/create/', CashReceiptCreateAPIView.as_view(), name='cash-receipt-create'),
    path('cash-disbursement/', CashDisbursementListAPIView.as_view(), name='cash-disbursement-list'),
    path('cash-disbursement/create/', CashDisbursementCreateAPIView.as_view(), name='cash-disbursement-create'),
    path('sales/', SalesListAPIView.as_view(), name='sales-list'),
    path('sales/create/', SalesCreateAPIView.as_view(), name='sales-create'),
]