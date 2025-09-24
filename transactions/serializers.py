from rest_framework import serializers
from .models import(
    JournalEntry,
    JournalLine,
    GeneralJournal,
    CashReceipt,
    CashDisbursement,
    Sales,
)

class JournalEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntry
        fields = '__all__'


class JournalLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalLine
        fields = '__all__'


class GeneralJournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralJournal
        fields = '__all__'


class CashReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashReceipt
        fields = '__all__'
    

class CashDisbursementSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashDisbursement
        fields = '__all__'


class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = '__all__'
    