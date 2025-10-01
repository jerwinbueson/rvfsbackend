from django.contrib import admin
from .models import JournalEntry, CashReceipt, CashDisbursement, Sales


admin.site.register(JournalEntry)
admin.site.register(CashReceipt)
admin.site.register(CashDisbursement)
admin.site.register(Sales)