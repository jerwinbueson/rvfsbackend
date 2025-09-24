from rest_framework import serializers
from .models import ChartsOfAccounts, AccountType, CashFlowType

class AccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountType
        fields = '__all__'

class CashFlowTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashFlowType
        fields = '__all__'

class ChartsOfAccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChartsOfAccounts
        fields = '__all__'