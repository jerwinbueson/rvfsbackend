from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView
from .serializers import ChartsOfAccountsSerializer, AccountTypeSerializer, CashFlowTypeSerializer
from .models import ChartsOfAccounts, AccountType, CashFlowType


class ChartsOfAccountsListView(ListAPIView):
    queryset = ChartsOfAccounts.objects.all()
    serializer_class = ChartsOfAccountsSerializer

class ChartsOfAccountsCreateView(CreateAPIView):
    queryset = ChartsOfAccounts.objects.all()
    serializer_class = ChartsOfAccountsSerializer

class AccountTypeListView(ListAPIView):
    queryset = AccountType.objects.all()
    serializer_class = AccountTypeSerializer

class AccountTypeCreateView(CreateAPIView):
    queryset = AccountType.objects.all()
    serializer_class = AccountTypeSerializer

class CashFlowTypeListView(ListAPIView):
    queryset = CashFlowType.objects.all()
    serializer_class = CashFlowTypeSerializer

class CashFlowTypeCreateView(CreateAPIView):
    queryset = CashFlowType.objects.all()
    serializer_class = CashFlowTypeSerializer
    
    