from rest_framework import serializers
from .models import(
    JournalEntry,
    PaymentType,
    TransactionType, 
    PaymentTerm,
)



class JournalEntrySerializer(serializers.ModelSerializer):
    account_name = serializers.StringRelatedField(source='account.name', read_only=True)
    formatted_amount = serializers.SerializerMethodField()


    class Meta:
        model = JournalEntry
        fields = '__all__'
        


class CashDisbursementSerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntry
        fields = [
            'id',
            'date',
            'reference', 
            'account', 
            'entry_type', 
            'description', 
            'supplier', 
            'payment_type', 
            'check_number', 
            'bank', 
            'amount', 
            'particulars'
            ]
    def create(self, validated_data):
        transaction_type = TransactionType.objects.get(name='Cash Disbursement')
        validated_data['transaction_type'] = transaction_type
        entry_type = 'Debit'
        validated_data['entry_type'] = entry_type
        return JournalEntry.objects.create(**validated_data)
            
        
    