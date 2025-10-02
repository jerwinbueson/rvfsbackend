from math import perm
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
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
    GeneralJournalSerializer
)

class JournalEntryListAPIView(ListAPIView):
    queryset = JournalEntry.objects.all()
    serializer_class = JournalEntrySerializer

    def get_queryset(self):
        if not hasattr(self.request.user, 'company') or not self.request.user.company:
            return JournalEntry.objects.none()
        return JournalEntry.objects.filter(business_unit=self.request.user.company).order_by('-date')

class JournalEntryCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = JournalEntry.objects.all()
    serializer_class = JournalEntrySerializer

    def perform_create(self, serializer):
        serializer.save(business_unit=self.request.user.company)
        calendar_year = self.request.user.company.calendaryear_set.get(default=True)
        serializer.save(calendar_year=calendar_year)


class JournalLineListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = JournalLine.objects.all()
    serializer_class = JournalLineSerializer


    def get_queryset(self):
        if not hasattr(self.request.user, 'company') or not self.request.user.company:
            return JournalLine.objects.none()
        return JournalLine.objects.filter(business_unit=self.request.user.company).select_related('journal_entry').order_by('-journal_entry__date')

class JournalLineCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = JournalLine.objects.all()
    serializer_class = JournalLineSerializer

    def perform_create(self, serializer):
        serializer.save(business_unit=self.request.user.company)
        calendar_year = self.request.user.company.calendaryear_set.get(default=True)
        serializer.save(calendar_year=calendar_year)
    

class CashReceiptListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CashReceipt.objects.all()
    serializer_class = CashReceiptSerializer

    def get_queryset(self):
        if not hasattr(self.request.user, 'company') or not self.request.user.company:
            return CashReceipt.objects.none()
        return CashReceipt.objects.filter(business_unit=self.request.user.company).order_by('-date')
 

class CashReceiptCreateAPIView(CreateAPIView):
    queryset = CashReceipt.objects.all()
    serializer_class = CashReceiptSerializer

    def perform_create(self, serializer):
        serializer.save(business_unit=self.request.user.company)
        calendar_year = self.request.user.company.calendaryear_set.get(default=True)
        serializer.save(calendar_year=calendar_year)

class CashDisbursementListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CashDisbursement.objects.all()
    serializer_class = CashDisbursementSerializer
    
class CashDisbursementCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CashDisbursement.objects.all()
    serializer_class = CashDisbursementSerializer

    def perform_create(self, serializer):
        serializer.save(business_unit=self.request.user.company)
        calendar_year = self.request.user.company.calendaryear_set.get(default=True)
        serializer.save(calendar_year=calendar_year)
    
class SalesListAPIView(ListAPIView):
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer
    
class SalesCreateAPIView(CreateAPIView):
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer
    

class GeneralJournalListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = JournalLine.objects.all()
    serializer_class = GeneralJournalSerializer
    
    def get_queryset(self):
        if not hasattr(self.request.user, 'company') or not self.request.user.company:
            return JournalLine.objects.none()
        return JournalLine.objects.filter(
            business_unit=self.request.user.company
        ).select_related('journal_entry').order_by('-journal_entry__date')