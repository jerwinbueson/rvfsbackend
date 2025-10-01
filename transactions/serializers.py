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
    account_name = serializers.StringRelatedField(source='account.name')
    class Meta:
        model = JournalLine
        fields = '__all__'
        read_only_fields = ('business_unit', 'calendar_year')

    def create(self, validated_data):
        request = self.context['request']
        validated_data['business_unit'] = request.user.company
        validated_data['calendar_year'] = request.user.company.calendaryear_set.get(default=True)
        return super().create(validated_data)


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
    