from django.db import models




class JournalEntry(models.Model):
    business_unit = models.ForeignKey('business.BusinessUnit', on_delete=models.PROTECT)
    calendar_year = models.ForeignKey('business.CalendarYear', on_delete=models.PROTECT)
    date = models.DateField()
    reference = models.CharField(max_length=20)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.reference} - {self.date}"
    

class GeneralJournal(models.Model):
    business_unit = models.ForeignKey('business.BusinessUnit', on_delete=models.PROTECT)
    calendar_year = models.ForeignKey('business.CalendarYear', on_delete=models.PROTECT)
    entry = models.ForeignKey(JournalEntry, on_delete=models.PROTECT)
    accounts = models.ForeignKey('chartsofaccounts.ChartsOfAccounts', on_delete=models.PROTECT)
    debit_amount = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    credit_amount = models.DecimalField(max_digits=30, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.reference} - {self.accounts}"


class CashReceipt(models.Model):
    business_unit = models.ForeignKey('business.BusinessUnit', on_delete=models.PROTECT)
    calendar_year = models.ForeignKey('business.CalendarYear', on_delete=models.PROTECT)
    date = models.DateField()
    particulars = models.CharField(max_length=255)  # Customer or description
    invoice_number = models.CharField(max_length=50, blank=True, null=True)
    cash_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    sales_return_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    sales_discount_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    wht_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    sales_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    journal_entry = models.OneToOneField(
        JournalEntry,
        on_delete=models.CASCADE,
        related_name='cash_receipt',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"CashReceipt {self.invoice_number} - {self.particulars}"


class CashDisbursement(models.Model):
    business_unit = models.ForeignKey('business.BusinessUnit', on_delete=models.PROTECT)
    calendar_year = models.ForeignKey('business.CalendarYear', on_delete=models.PROTECT)
    date = models.DateField()
    particulars = models.CharField(max_length=255)  # Supplier or description
    invoice_number = models.CharField(max_length=50, blank=True, null=True)
    cash_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    purchase_return_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    purchase_discount_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    wht_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    purchase_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    journal_entry = models.OneToOneField(
        JournalEntry,
        on_delete=models.CASCADE,
        related_name='cash_disbursement',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"CashDisbursement {self.invoice_number} - {self.particulars}"

    
class Sales(models.Model):
    business_unit = models.ForeignKey('business.BusinessUnit', on_delete=models.PROTECT)
    calendar_year = models.ForeignKey('business.CalendarYear', on_delete=models.PROTECT)
    journal_entry = models.OneToOneField(JournalEntry, on_delete=models.CASCADE, related_name='sale')
    invoice_number = models.CharField(max_length=50)
    customer = models.CharField(max_length=255)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    terms = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Sale {self.invoice_number} - {self.customer}"
