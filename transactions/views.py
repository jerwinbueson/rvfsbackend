from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import (
    JournalEntry,
    TransactionType,
    PaymentType,
    PaymentTerm,
)
from .serializers import (
    JournalEntrySerializer,
    CashDisbursementSerializer,
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


class JournalEntryCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = JournalEntrySerializer

    def perform_create(self, serializer):
        _add_user_headers(serializer, self.request.user)

class CashDisbursementCreateAPIView(CreateAPIView):
    serializer_class = CashDisbursementSerializer

    def perform_create(self, serializer):
        _add_user_headers(serializer, self.request.user)
    
