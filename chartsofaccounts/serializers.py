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
    business_unit = serializers.StringRelatedField()
    account_type_name = serializers.StringRelatedField(source='type')
    cash_flow_type_name = serializers.StringRelatedField(source='cash_flow_type')

    class Meta:
        model = ChartsOfAccounts
        fields = '__all__'

    def validate(self, data):
        request = self.context.get('request')
        business_unit = getattr(request.user, 'company', None)
        if business_unit and ChartsOfAccounts.objects.filter(
            business_unit=business_unit, 
            code=data['code'], 
            name=data['name']
            ).exists():
                raise serializers.ValidationError({"non_field_errors": ["Account Code and Name must be unique."]})
        return data

class COAListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChartsOfAccounts
        fields = ['id', 'name']