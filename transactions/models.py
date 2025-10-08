from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class TransactionType(models.Model):
    business_unit = models.ForeignKey('business.BusinessUnit', on_delete=models.PROTECT)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

class PaymentType(models.Model):
    business_unit = models.ForeignKey('business.BusinessUnit', on_delete=models.PROTECT)
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
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.PROTECT)
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
    account = models.ForeignKey('chartsofaccounts.ChartsOfAccounts', on_delete=models.PROTECT, null=True, blank=True)
    reference = models.CharField(max_length=50, blank=True, null=True)
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.PROTECT)
    description = models.CharField(max_length=255)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.PROTECT)
    check_number = models.CharField(max_length=50, blank=True, null=True)
    cash_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)


class CashDisbursement(models.Model):
    business_unit = models.ForeignKey('business.BusinessUnit', on_delete=models.PROTECT, null=True, blank=True)
    calendar_year = models.ForeignKey('business.CalendarYear', on_delete=models.PROTECT, null=True, blank=True)
    date = models.DateField()
    account = models.ForeignKey('chartsofaccounts.ChartsOfAccounts', on_delete=models.PROTECT, related_name='cash_disbursements', null=True, blank=True)
    reference = models.CharField(max_length=50, blank=True, null=True)
    supplier = moedels.ForeignKey('suppliers.Supplier', on_delete=models.PROTECT, blank=True, null=True)
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.PROTECT)
    description = models.CharField(max_length=255)  # Supplier or description
    payment_type = models.ForeignKey(PaymentType, on_delete=models.PROTECT)
    check_number = models.CharField(max_length=50, blank=True, null=True)
    cash_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.reference} - {self.supplier.name}"
    

class Sales(models.Model):
    business_unit = models.ForeignKey('business.BusinessUnit', on_delete=models.PROTECT, null=True, blank=True)
    calendar_year = models.ForeignKey('business.CalendarYear', on_delete=models.PROTECT, null=True, blank=True)
    date = models.DateField()    
    account = models.ForeignKey('chartsofaccounts.ChartsOfAccounts', on_delete=models.PROTECT)
    reference = models.CharField(max_length=50, blank=True, null=True)
    customer = models.ForeignKey('customers.Customer', on_delete=models.PROTECT)
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.PROTECT)
    description = models.CharField(max_length=255)
    invoice_number = models.CharField(max_length=50)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    terms = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Sale {self.invoice_number} - {self.customer}"