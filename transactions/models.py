from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class TransactionType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)


class JournalEntry(models.Model):
    CHOICES = (
        ('Debit', 'Debit'),
        ('Credit', 'Credit'),
    )  
    business_unit = models.ForeignKey('business.BusinessUnit', on_delete=models.PROTECT)
    calendar_year = models.ForeignKey('business.CalendarYear', on_delete=models.PROTECT)
    date = models.DateField()
    reference = models.CharField(max_length=20)  # control number/voucher no
    account = models.ForeignKey('chartsofaccounts.ChartsOfAccounts', on_delete=models.PROTECT)
    type = models.CharField(max_length=10, choices=CHOICES, null=True, blank=True) #Remove this null and blank during production
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        null=True,
        blank=True,
        validators=[MinValueValidator(0.01, message="Amount must be greater than 0")]
    ) #Remove this null and blank during production
    particulars = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.journal_entry.reference} - {self.account.name}"


class CashReceipt(models.Model):
    business_unit = models.ForeignKey('business.BusinessUnit', on_delete=models.PROTECT, null=True, blank=True)
    calendar_year = models.ForeignKey('business.CalendarYear', on_delete=models.PROTECT, null=True, blank=True)
    date = models.DateField()
    account = models.ForeignKey('chartsofaccounts.ChartsOfAccounts', on_delete=models.PROTECT, related_name='cash_receipts', null=True, blank=True)
    description = models.CharField(max_length=255)
    reference = models.CharField(max_length=50, blank=True, null=True)
    cash_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    sales_return_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0, null=True, blank=True)
    sales_discount_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0, null=True, blank=True)
    wht_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0, null=True, blank=True)
    sales_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)


class CashDisbursement(models.Model):
    business_unit = models.ForeignKey('business.BusinessUnit', on_delete=models.PROTECT, null=True, blank=True)
    calendar_year = models.ForeignKey('business.CalendarYear', on_delete=models.PROTECT, null=True, blank=True)
    account = models.ForeignKey('chartsofaccounts.ChartsOfAccounts', on_delete=models.PROTECT, related_name='cash_disbursements', null=True, blank=True)
    date = models.DateField()
    description = models.CharField(max_length=255)  # Supplier or description
    reference = models.CharField(max_length=50, blank=True, null=True)
    cash_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    purchase_return_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0, null=True, blank=True)
    purchase_discount_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0, null=True, blank=True)
    wht_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0, null=True, blank=True)
    disbursement_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    

class Sales(models.Model):
    invoice_number = models.CharField(max_length=50)
    customer = models.CharField(max_length=255)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    terms = models.CharField(max_length=100, blank=True, null=True)

    # FIX 5: Corrected __str__ method typo
    def __str__(self):
        return f"Sale {self.invoice_number} - {self.customer}"