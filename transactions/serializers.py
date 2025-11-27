from rest_framework import serializers
from .models import(
    JournalEntry,
    PaymentType,
    PaymentTerm,
)
from chartsofaccounts.models import ChartsOfAccounts



class JournalEntrySerializer(serializers.ModelSerializer):
    account_name = serializers.StringRelatedField(source='account.name', read_only=True)
    formatted_amount = serializers.SerializerMethodField()
    account_type = serializers.StringRelatedField(source='account.type', read_only=True)
    account = serializers.PrimaryKeyRelatedField(
        queryset=ChartsOfAccounts.objects.none()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and hasattr(request.user, 'company'):
            self.fields['account'].queryset = ChartsOfAccounts.objects.filter(
                business_unit=request.user.company
            )

    def get_formatted_amount(self, obj):
        if obj.amount is None:
            return "0.00"
        return f"{obj.amount:,.2f}"

    class Meta:
        model = JournalEntry
        fields = '__all__'
        read_only_fields = ['business_unit', 'calendar_year']


class JournalEntryFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntry
        fields = ['accounts', 'account_type', 'transaction_type', 'entry_type']

class CashDisbursementSerializer(serializers.ModelSerializer):
    formatted_amount = serializers.SerializerMethodField()
    account = serializers.PrimaryKeyRelatedField(
        queryset=ChartsOfAccounts.objects.none()
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and hasattr(request.user, 'company'):
            self.fields['account'].queryset = ChartsOfAccounts.objects.filter(
                business_unit=request.user.company
            )
    
    def get_formatted_amount(self, obj):
        if obj.amount is None:
            return "0.00"
        return f"{obj.amount:,.2f}"
    
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
            'formatted_amount',
            'particulars',
            'transaction_type'
            ]
        read_only_fields = ['business_unit', 'calendar_year']
    def create(self, validated_data):
        transaction_type = 'Cash Disbursement'
        validated_data['transaction_type'] = transaction_type
        entry_type = 'Debit'
        validated_data['entry_type'] = entry_type
        return JournalEntry.objects.create(**validated_data)

class CashReceiptSerializer(serializers.ModelSerializer):
    formatted_amount = serializers.SerializerMethodField()
    account = serializers.PrimaryKeyRelatedField(
        queryset=ChartsOfAccounts.objects.none()
    )    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and hasattr(request.user, 'company'):
            self.fields['account'].queryset = ChartsOfAccounts.objects.filter(
                business_unit=request.user.company
            )
            
    def get_formatted_amount(self, obj):
        if obj.amount is None:
            return "0.00"
        return f"{obj.amount:,.2f}"
    
    class Meta:
        model = JournalEntry
        fields = [
            'id',
            'date',
            'reference', 
            'account', 
            'description', 
            'customer', 
            'payment_type', 
            'check_number', 
            'bank', 
            'amount',
            'formatted_amount',
            'particulars',
            ]
        read_only_fields = ['business_unit', 'calendar_year']
    def create(self, validated_data):
        transaction_type = 'Cash Receipt'
        validated_data['transaction_type'] = transaction_type
        entry_type = 'Credit'
        validated_data['entry_type'] = entry_type
        return JournalEntry.objects.create(**validated_data)

class SalesInvoiceSerializer(serializers.ModelSerializer):
    formatted_amount = serializers.SerializerMethodField()
    account = serializers.PrimaryKeyRelatedField(
        queryset=ChartsOfAccounts.objects.none()
    )    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and hasattr(request.user, 'company'):
            self.fields['account'].queryset = ChartsOfAccounts.objects.filter(
                business_unit=request.user.company
            )
            
    def get_formatted_amount(self, obj):
        if obj.amount is None:
            return "0.00"
        return f"{obj.amount:,.2f}"
    
    class Meta:
        model = JournalEntry
        fields = [
            'id',
            'date',
            'reference', 
            'account', 
            'entry_type', 
            'description', 
            'customer', 
            'payment_type', 
            'check_number', 
            'bank', 
            'amount',
            'formatted_amount',
            'particulars',
            'transaction_type'
            ]
        read_only_fields = ['business_unit', 'calendar_year']
    def create(self, validated_data):
        transaction_type = 'Sales Invoice'
        validated_data['transaction_type'] = transaction_type
        entry_type = 'Credit'
        validated_data['entry_type'] = entry_type
        return JournalEntry.objects.create(**validated_data)
    

class PurchaseInvoiceSerializer(serializers.ModelSerializer):
    formatted_amount = serializers.SerializerMethodField()
    account = serializers.PrimaryKeyRelatedField(
        queryset=ChartsOfAccounts.objects.none()
    )    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and hasattr(request.user, 'company'):
            self.fields['account'].queryset = ChartsOfAccounts.objects.filter(
                business_unit=request.user.company
            )
            
    def get_formatted_amount(self, obj):
        if obj.amount is None:
            return "0.00"
        return f"{obj.amount:,.2f}"
    
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
            'formatted_amount',
            'particulars',
            'transaction_type'
            ]
        read_only_fields = ['business_unit', 'calendar_year']
    def create(self, validated_data):
        transaction_type = 'Purchase Invoice'
        validated_data['transaction_type'] = transaction_type
        entry_type = 'Debit'
        validated_data['entry_type'] = entry_type
        return JournalEntry.objects.create(**validated_data)
    
class GeneralJournalSerializer(serializers.ModelSerializer):
    account_name = serializers.SerializerMethodField()
    class Meta:
        model = JournalEntry
        fields = ['date', 'account_name', 'reference', 'transaction_type', 'entry_type', 'amount', 'particulars']

    def get_account_name(self, obj):
        return obj.account.name