from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    JournalEntry,
    PaymentType,
    PaymentTerm,
)
from .serializers import (
    JournalEntrySerializer,
    JournalEntryFilterSerializer,
    CashDisbursementSerializer,
    CashReceiptSerializer,
    SalesInvoiceSerializer, 
    PurchaseInvoiceSerializer,
    GeneralJournalSerializer,
    
)
from .filters import (
    JournalEntryFilter,
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
    filter_backends = [DjangoFilterBackend]
    filterset_class = JournalEntryFilter
    
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


class JournalEntryFilterView(ListAPIView):
    serializer_class = JournalEntryFilterSerializer
    permission_classes = [IsAuthenticated]
    
    
    def get_queryset(self):
        """Return journal entries for the authenticated user's company."""
        user = self.request.user

        # If user has no company or business unit, return none
        if not hasattr(user, 'company') or not user.company:
            return JournalEntry.objects.none()

        # Filter by user's business unit (company) and default calendar year
        try:
            cal = user.company.calendaryear_set.get(default=True)
        except CalendarYear.DoesNotExist:
            return JournalEntry.objects.none()
        return JournalEntry.objects.filter(
            business_unit=user.company,
            calendar_year=cal
        )
    
    def list(self, request, *args, **kwargs):
        """Return distinct lists for each filter dropdown."""
        qs = self.get_queryset()

        accounts = qs.values_list("account__name", flat=True).distinct()
        account_types = qs.values_list("account__type__name", flat=True).distinct()
        transaction_types = qs.values_list("transaction_type", flat=True).distinct()
        entry_types = qs.values_list("entry_type", flat=True).distinct()

        data = {
            "accounts": list(accounts),
            "account_types": list(account_types),
            "transaction_types": list(transaction_types),
            "entry_types": list(entry_types),
        }
        return Response(data)



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

class GeneralJournalView(ListAPIView):
    serializer_class = GeneralJournalSerializer
    queryset = JournalEntry

    def get_queryset(self):
        if not hasattr(self.request.user, 'company') or not self.request.user.company:
            return JournalEntry.objects.none()
        return JournalEntry.objects.filter(business_unit=self.request.user.company)