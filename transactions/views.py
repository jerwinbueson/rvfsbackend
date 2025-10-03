from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import (
    JournalEntry, JournalLine,
    CashReceipt, CashDisbursement, Sales,
)
from .serializers import (
    JournalEntrySerializer, JournalLineSerializer,
    CashReceiptSerializer, CashDisbursementSerializer,
    SalesSerializer, GeneralJournalSerializer,
)

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

class JournalEntryListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = JournalEntrySerializer

    def get_queryset(self):
        return JournalEntry.objects.filter(
            business_unit=self.request.user.company
        ).select_related('business_unit', 'calendar_year').order_by('-date')


class JournalEntryCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = JournalEntrySerializer

    def perform_create(self, serializer):
        _add_user_headers(serializer, self.request.user)


class JournalLineListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = JournalLineSerializer

    def get_queryset(self):
        return JournalLine.objects.filter(
            business_unit=self.request.user.company
        ).select_related(
            'journal_entry', 'account', 'business_unit', 'calendar_year'
        ).order_by('-journal_entry__date', '-id')


class JournalLineCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = JournalLineSerializer

    def perform_create(self, serializer):
        _add_user_headers(serializer, self.request.user)


class CashReceiptListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CashReceiptSerializer

    def get_queryset(self):
        return CashReceipt.objects.filter(
            business_unit=self.request.user.company
        ).select_related(
            'business_unit', 'calendar_year', 'account', 'journal_entry'
        ).order_by('-date')


class CashReceiptCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CashReceiptSerializer

    def perform_create(self, serializer):
        _add_user_headers(serializer, self.request.user)


class CashDisbursementListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CashDisbursementSerializer

    def get_queryset(self):
        return CashDisbursement.objects.filter(
            business_unit=self.request.user.company
        ).select_related(
            'business_unit', 'calendar_year', 'account', 'journal_entry'
        ).order_by('-date')


class CashDisbursementCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CashDisbursementSerializer

    def perform_create(self, serializer):
        _add_user_headers(serializer, self.request.user)


class SalesListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SalesSerializer

    def get_queryset(self):
        return Sales.objects.filter(
            journal_entry__business_unit=self.request.user.company
        ).select_related('journal_entry').order_by('-journal_entry__date')


class SalesCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SalesSerializer


class GeneralJournalListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GeneralJournalSerializer

    def get_queryset(self):
        return JournalLine.objects.filter(
            business_unit=self.request.user.company
        ).select_related(
            'journal_entry', 'account', 'business_unit', 'calendar_year'
        ).order_by('-journal_entry__date', '-id')