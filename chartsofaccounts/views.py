from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView
from .serializers import ChartsOfAccountsSerializer, AccountTypeSerializer, CashFlowTypeSerializer
from .models import ChartsOfAccounts, AccountType, CashFlowType
from rest_framework.permissions import IsAuthenticated

class ChartsOfAccountsListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ChartsOfAccounts.objects.all()
    serializer_class = ChartsOfAccountsSerializer

    def get_queryset(self):
        if not hasattr(self.request.user, 'company') or not self.request.user.company:
            return ChartsOfAccounts.objects.none()
        return ChartsOfAccounts.objects.filter(business_unit=self.request.user.company)



class ChartsOfAccountsCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ChartsOfAccounts.objects.all()
    serializer_class = ChartsOfAccountsSerializer

    def perform_create(self, serializer):
        serializer.save(business_unit=self.request.user.company)

class AccountTypeListView(ListAPIView):
    queryset = AccountType.objects.all()
    serializer_class = AccountTypeSerializer

    def get_queryset(self):
        if not hasattr(self.request.user, 'company') or not self.request.user.company:
            return AccountType.objects.none()
        return AccountType.objects.filter(business_unit=self.request.user.company)

class AccountTypeCreateView(CreateAPIView):
    queryset = AccountType.objects.all()
    serializer_class = AccountTypeSerializer

class CashFlowTypeListView(ListAPIView):
    queryset = CashFlowType.objects.all()
    serializer_class = CashFlowTypeSerializer

    def get_queryset(self):
        if not hasattr(self.request.user, 'company') or not self.request.user.company:
            return CashFlowType.objects.none()
        return CashFlowType.objects.filter(business_unit=self.request.user.company)

class CashFlowTypeCreateView(CreateAPIView):
    queryset = CashFlowType.objects.all()
    serializer_class = CashFlowTypeSerializer
    
    