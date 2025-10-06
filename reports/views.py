from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Case, When, F, DecimalField
from transactions.models import JournalLine
from .serializers import GeneralLedgerSerializer
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

class GeneralLedgerAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = GeneralLedgerSerializer

    def get_queryset(self):
        # Ensure the user is authenticated and has a company
        if not self.request.user.is_authenticated or not hasattr(self.request.user, 'company'):
            return JournalLine.objects.none()
        
        qs = (
            JournalLine.objects
            .filter(
                business_unit=self.request.user.company,
                journal_entry__isnull=False  # Ensure journal_entry exists
            )
            .select_related('journal_entry', 'account')
            .order_by('-journal_entry__date', '-id')
        )
        
        # Optional filters
        account = self.request.query_params.get('account')       if account:
            qs = qs.filter(account__code=account)
        
        return qs