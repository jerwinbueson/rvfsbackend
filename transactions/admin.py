from django.contrib import admin
from .models import JournalEntry, PaymentType, PaymentTerm


admin.site.register(JournalEntry)
admin.site.register(PaymentType)
admin.site.register(PaymentTerm)
