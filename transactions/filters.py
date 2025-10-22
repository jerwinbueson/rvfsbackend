# transactions/filters.py
import django_filters
from .models import JournalEntry

class JournalEntryFilter(django_filters.FilterSet):
    account = django_filters.CharFilter(field_name='account__name', lookup_expr='icontains')
    account_type = django_filters.CharFilter(field_name='account__account_type', lookup_expr='icontains')
    transaction_type = django_filters.CharFilter(lookup_expr='icontains')
    entry_type = django_filters.CharFilter(lookup_expr='icontains')
    reference = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = JournalEntry
        fields = ['account', 'account_type', 'transaction_type', 'entry_type', 'reference']
