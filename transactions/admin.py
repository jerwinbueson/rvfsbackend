from django.contrib import admin
from .models import JournalEntry, JournalLine, CashReceipt, CashDisbursement, Sales


admin.site.register(JournalEntry)
admin.site.register(JournalLine)
admin.site.register(CashReceipt)
admin.site.register(CashDisbursement)
admin.site.register(Sales)