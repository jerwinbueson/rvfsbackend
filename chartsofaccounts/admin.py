from django.contrib import admin

from .models import AccountType, CashFlowType, ChartsOfAccounts

admin.site.register(AccountType)
admin.site.register(CashFlowType)
admin.site.register(ChartsOfAccounts)
