from rest_framework import serializers
from .models import(
    JournalEntry,
    JournalLine,
    CashReceipt,
    CashDisbursement,
    Sales,
)

class JournalEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntry
        fields = '__all__'
        read_only_fields = ('business_unit', 'calendar_year')

    def create(self, validated_data):
        request = self.context['request']
        validated_data['business_unit'] = request.user.company
        validated_data['calendar_year'] = request.user.company.calendaryear_set.get(default=True)
        return super().create(validated_data)


class JournalLineSerializer(serializers.ModelSerializer):
    journal_entry_details = JournalEntrySerializer(
        source='journal_entry', 
        read_only=True
    )
    account_name = serializers.StringRelatedField(source='account.name', read_only=True)
    formatted_amount = serializers.SerializerMethodField()


    class Meta:
        model = JournalLine
        fields = '__all__'
        
    def get_formatted_amount(self, obj):
        if obj.amount is not None:
            return f"{obj.amount:,.2f}"
        return None


    def create(self, validated_data):
        request = self.context['request']
        validated_data['business_unit'] = request.user.company
        validated_data['calendar_year'] = request.user.company.calendaryear_set.get(default=True)
        return super().create(validated_data)


class CashReceiptSerializer(serializers.ModelSerializer):
    account_name = serializers.StringRelatedField(source='account.name', read_only=True)
    formatted_amount = serializers.SerializerMethodField()
    class Meta:
        model = CashReceipt
        fields = '__all__'
    
    def get_formatted_amount(self, obj):
        if obj.cash_amount is not None:
            return f"{obj.cash_amount:,.2f}"
        return None

    def create(self, validated_data):
        request = self.context['request']
        validated_data['business_unit'] = request.user.company
        validated_data['calendar_year'] = request.user.company.calendaryear_set.get(default=True)
        return super().create(validated_data)

class CashDisbursementSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashDisbursement
        fields = '__all__'


class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = '__all__'
    

class GeneralJournalSerializer(serializers.ModelSerializer):
    journal_entry_details = JournalEntrySerializer(
        source='journal_entry', 
        read_only=True
    )
    account_name = serializers.StringRelatedField(source='account.name', read_only=True)
    account_type = serializers.StringRelatedField(source='account.account_type', read_only=True)
    cash_flow_type = serializers.StringRelatedField(source='account.cash_flow_type', read_only=True)
    formatted_amount = serializers.SerializerMethodField()

    class Meta:
        model = JournalLine
        fields = '__all__'
        read_only_fields = ('business_unit', 'calendar_year')

    def get_formatted_amount(self, obj):
        if obj.amount is not None:
            return f"{obj.amount:,.2f}"
        return None