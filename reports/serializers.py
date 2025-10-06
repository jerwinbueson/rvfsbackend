from rest_framework import serializers
from transactions.models import JournalLine

# serializers.py
class GeneralLedgerSerializer(serializers.ModelSerializer):
    date           = serializers.DateField(source='journal_entry.date')
    reference      = serializers.CharField(source='journal_entry.reference')
    description    = serializers.CharField(source='journal_entry.description')
    account_code   = serializers.CharField(source='account.code')
    account_name   = serializers.CharField(source='account.name')
    debit          = serializers.SerializerMethodField()
    credit         = serializers.SerializerMethodField()

    class Meta:
        model  = JournalLine
        fields = ['date','reference','description','account_code','account_name',
                  'debit','credit','particulars']

    def get_debit(self, obj):
        return obj.amount if obj.type == 'Debit' else 0

    def get_credit(self, obj):
        return obj.amount if obj.type == 'Credit' else 0