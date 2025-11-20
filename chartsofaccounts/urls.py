from nturl2path import url2pathname
from django.urls import path
from .views import (
    ChartsOfAccountsView,
    ChartsOfAccountsRUDView,
    AccountTypeView, 
    CashFlowTypeView, 
    COAListView
)

urlpatterns = [
    path('', ChartsOfAccountsView.as_view(), name='charts-of-accounts-list'),
    path('<int:pk>/', ChartsOfAccountsRUDView.as_view()),
    path('account-type/', AccountTypeView.as_view(), name='account-type-list'),
    path('cash-flow/', CashFlowTypeView.as_view(), name='cash-flow-type-list'),
    path('coa/', COAListView.as_view()),
]
    