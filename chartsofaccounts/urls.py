from nturl2path import url2pathname
from django.urls import path
from .views import (
    ChartsOfAccountsListView, 
    ChartsOfAccountsCreateView, 
    AccountTypeListView, 
    AccountTypeCreateView, 
    CashFlowTypeListView, 
    CashFlowTypeCreateView       
)

urlpatterns = [
    path('', ChartsOfAccountsListView.as_view(), name='charts-of-accounts-list'),
    path('create/', ChartsOfAccountsCreateView.as_view(), name='charts-of-accounts-create'),
    path('account-type/', AccountTypeListView.as_view(), name='account-type-list'),
    path('account-type/create/', AccountTypeCreateView.as_view(), name='account-type-create'),
    path('cash-flow-type/', CashFlowTypeListView.as_view(), name='cash-flow-type-list'),
    path('cash-flow-type/create/', CashFlowTypeCreateView.as_view(), name='cash-flow-type-create'),
]
    