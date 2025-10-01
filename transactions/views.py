from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView
from .models import(
    JournalEntry,
    JournalLine,
    CashReceipt,
    CashDisbursement,
    Sales,
)
from .serializers import(
    JournalEntrySerializer,
    JournalLineSerializer,
    CashReceiptSerializer,
    CashDisbursementSerializer,
    SalesSerializer,
)

class JournalEntryListAPIView(ListAPIView):
    queryset = JournalEntry.objects.all()
    serializer_class = JournalEntrySerializer

class JournalEntryCreateAPIView(CreateAPIView):
    queryset = JournalEntry.objects.all()
    serializer_class = JournalEntrySerializer


class JournalLineListAPIView(ListAPIView):
    queryset = JournalLine.objects.all()
    serializer_class = JournalLineSerializer

class JournalLineCreateAPIView(CreateAPIView):
    queryset = JournalLine.objects.all()
    serializer_class = JournalLineSerializer
    

class CashReceiptListAPIView(ListAPIView):
    queryset = CashReceipt.objects.all()
    serializer_class = CashReceiptSerializer
    

class CashReceiptCreateAPIView(CreateAPIView):
    queryset = CashReceipt.objects.all()
    serializer_class = CashReceiptSerializer

class CashDisbursementListAPIView(ListAPIView):
    queryset = CashDisbursement.objects.all()
    serializer_class = CashDisbursementSerializer
    
class CashDisbursementCreateAPIView(CreateAPIView):
    queryset = CashDisbursement.objects.all()
    serializer_class = CashDisbursementSerializer
    
class SalesListAPIView(ListAPIView):
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer
    
class SalesCreateAPIView(CreateAPIView):
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer
    