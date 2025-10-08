from rest_framework import serializers
from .models import(
    JournalEntry,
    CashReceipt,
    CashDisbursement,
    Sales,
)



class JournalEntrySerializer(serializers.ModelSerializer):
    account_name = serializers.StringRelatedField(source='account.name', read_only=True)
    formatted_amount = serializers.SerializerMethodField()


    class Meta:
        model = JournalEntry
        fields = '__all__'
        


class CashReceiptSerializer(serializers.ModelSerializer):
    account_name = serializers.StringRelatedField(source='account.name', read_only=True)
    formatted_amount = serializers.SerializerMethodField()
    class Meta:
        model = CashReceipt
        fields = '__all__'
    

class CashDisbursementSerializer(serializers.ModelSerializer):
    account_name = serializers.StringRelatedField(source='account.name', read_only=True)
    formatted_amount = serializers.SerializerMethodField()
    formatted_disbursement_amount = serializers.SerializerMethodField()
    
    class Meta:
        model = CashDisbursement
        fields = '__all__'
        read_only_fields = ('account_name',)
    
    

class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = '__all__'
    

class GeneralJournalSerializer(serializers.ModelSerializer):
    account_name = serializers.StringRelatedField(source='account.name', read_only=True)
    account_type = serializers.StringRelatedField(source='account.account_type', read_only=True)
    cash_flow_type = serializers.StringRelatedField(source='account.cash_flow_type', read_only=True)
    formatted_amount = serializers.SerializerMethodField()

    class Meta:
        model = JournalEntry
        fields = '__all__'
        read_only_fields = ('business_unit', 'calendar_year')

    def get_formatted_amount(self, obj):
        if obj.amount is not None:
            return f"{obj.amount:,.2f}"
        return None