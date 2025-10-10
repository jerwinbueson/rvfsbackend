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
        


