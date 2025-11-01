from django.urls import path
from .views import(
    JournalEntryCreateAPIView,
    JournalEntryListAPIView,
    JournalEntryFilterView,
    CashDisbursementCreateAPIView,
    CashDisbursementListAPIView,
    CashReceiptCreateAPIView,
    CashReceiptListAPIView,
    SalesInvoiceCreateAPIView,
    SalesInvoiceListAPIView,
    PurchaseInvoiceCreateAPIView,
    PurchaseInvoiceListAPIView,
    
)

urlpatterns = [
    path('journal-entry/create/', JournalEntryCreateAPIView.as_view(), name='journal-line-list'),
    path('journal-entry/', JournalEntryListAPIView.as_view(), name='journal-line-list'),
    path('journal-entry/filter/', JournalEntryFilterView.as_view(), name='journal-entry-fiter'),
    path('cash-disbursement/create/', CashDisbursementCreateAPIView.as_view(), name='cash-disbursement-create'),
    path('cash-disbursement/', CashDisbursementListAPIView.as_view(), name='cash-disbursement-list'),
    path('cash-receipt/create/', CashReceiptCreateAPIView.as_view(), name='cash-receipt-create'),
    path('cash-receipt/', CashReceiptListAPIView.as_view(), name='cash-receipt-list'),
    path('sales-invoice/create/', SalesInvoiceCreateAPIView.as_view(), name='sales-invoice-create'),
    path('sales-invoice/', SalesInvoiceListAPIView.as_view(), name='sales-invoice-list'),
    path('purchase-invoice/create/', PurchaseInvoiceCreateAPIView.as_view(), name='purchase-invoice-create'),
    path('purchase-invoice/', PurchaseInvoiceListAPIView.as_view(), name='purchase-invoice-list'),
]