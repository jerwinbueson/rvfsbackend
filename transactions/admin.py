from django.contrib import admin
from .models import JournalEntry, PaymentType, TransactionType, PaymentTerm


admin.site.register(JournalEntry)
admin.site.register(PaymentType)
admin.site.register(TransactionType)
admin.site.register(PaymentTerm)
