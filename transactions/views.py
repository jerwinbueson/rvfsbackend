from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import (
    JournalEntry,
    PaymentType,
    PaymentTerm,
)
from .serializers import (
    JournalEntrySerializer,
    CashDisbursementSerializer,
    CashReceiptSerializer,
    SalesInvoiceSerializer, 
    PurchaseInvoiceSerializer,
)
from business.models import BusinessUnit, CalendarYear

# ---------- helpers -------------------------------------------------
def _add_user_headers(serializer, user):
    """Add business_unit + default calendar_year in ONE save()."""
    if not hasattr(user, 'company') or not user.company:
        raise PermissionDenied('User has no assigned company.')
    cal = user.company.calendaryear_set.get(default=True)
    return serializer.save(
        business_unit=user.company,
        calendar_year=cal,
    )
# -------------------------------------------------------------------


class JournalEntryCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = JournalEntrySerializer

    def perform_create(self, serializer):
        _add_user_headers(serializer, self.request.user)


class JournalEntryListAPIView(ListAPIView):
    serializer_class = JournalEntrySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if not hasattr(self.request.user, 'company') or not self.request.user.company:
            return JournalEntry.objects.none()
        
        try:
            cal = self.request.user.company.calendaryear_set.get(default=True)
        except CalendarYear.DoesNotExist:
            return JournalEntry.objects.none()
            
        return JournalEntry.objects.filter(
            business_unit=self.request.user.company,
            calendar_year=cal
        ).select_related('account', 'supplier', 'customer', 'payment_type', 'bank')

class CashDisbursementCreateAPIView(CreateAPIView):
    serializer_class = CashDisbursementSerializer

    def perform_create(self, serializer):
        _add_user_headers(serializer, self.request.user)
        

class CashDisbursementListAPIView(ListAPIView):
    serializer_class = CashDisbursementSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if not hasattr(self.request.user, 'company') or not self.request.user.company:
            return JournalEntry.objects.none()
        
        try:
            cal = self.request.user.company.calendaryear_set.get(default=True)
        except CalendarYear.DoesNotExist:
            return JournalEntry.objects.none()
            
        return JournalEntry.objects.filter(
            business_unit=self.request.user.company,
            calendar_year=cal,
            transaction_type='Cash Disbursement'
        ).select_related('account', 'supplier', 'customer', 'payment_type', 'bank')
    


class CashReceiptCreateAPIView(CreateAPIView):
    serializer_class = CashReceiptSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        _add_user_headers(serializer, self.request.user)

class CashReceiptListAPIView(ListAPIView):
    serializer_class = CashReceiptSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if not hasattr(self.request.user, 'company') or not self.request.user.company:
            return JournalEntry.objects.none()
        
        try:
            cal = self.request.user.company.calendaryear_set.get(default=True)
        except CalendarYear.DoesNotExist:
            return JournalEntry.objects.none()
            
        return JournalEntry.objects.filter(
            business_unit=self.request.user.company,
            calendar_year=cal,
            transaction_type='Cash Receipt'
        ).select_related('account', 'supplier', 'customer', 'payment_type', 'bank')
    

class SalesInvoiceCreateAPIView(CreateAPIView):
    serializer_class = SalesInvoiceSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        _add_user_headers(serializer, self.request.user)

class SalesInvoiceListAPIView(ListAPIView):
    serializer_class = SalesInvoiceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if not hasattr(self.request.user, 'company') or not self.request.user.company:
            return JournalEntry.objects.none()
        
        try:
            cal = self.request.user.company.calendaryear_set.get(default=True)
        except CalendarYear.DoesNotExist:
            return JournalEntry.objects.none()
            
        return JournalEntry.objects.filter(
            business_unit=self.request.user.company,
            calendar_year=cal,
            transaction_type='Sales Invoice'
        ).select_related('account', 'supplier', 'customer', 'payment_type', 'bank')

class PurchaseInvoiceCreateAPIView(CreateAPIView):
    serializer_class = PurchaseInvoiceSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        _add_user_headers(serializer, self.request.user)

class PurchaseInvoiceListAPIView(ListAPIView):
    serializer_class = PurchaseInvoiceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if not hasattr(self.request.user, 'company') or not self.request.user.company:
            return JournalEntry.objects.none()
        
        try:
            cal = self.request.user.company.calendaryear_set.get(default=True)
        except CalendarYear.DoesNotExist:
            return JournalEntry.objects.none()
            
        return JournalEntry.objects.filter(
            business_unit=self.request.user.company,
            calendar_year=cal,
            transaction_type='Purchase Invoice'
        ).select_related('account', 'supplier', 'customer', 'payment_type', 'bank')