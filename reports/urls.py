from django.urls import path
from .views import GeneralLedgerAPIView
urlpatterns =[
    path('general-ledger/', GeneralLedgerAPIView.as_view(), name='general-ledger'),
]