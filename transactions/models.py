from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from bank.models import Bank



class PaymentType(models.Model):
    business_unit = models.ForeignKey('business.BusinessUnit', on_delete=models.PROTECT)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name




class JournalEntry(models.Model):
    TRANSACTION_TYPE = (
        ('Cash Disbursement', 'Cash Disbursement'),
        ('Cash Receipt', 'Cash Receipt'),
        ('Journal Entry', 'Journal Entry'),
        ('Sales Invoice', 'Sales Invoice'),
        ('Purchase Invoice', 'Purchase Invoice'),
    )
    
    
    CHOICES = (
        ('Debit', 'Debit'),
        ('Credit', 'Credit'),
    )  
    business_unit = models.ForeignKey('business.BusinessUnit', on_delete=models.PROTECT)
    calendar_year = models.ForeignKey('business.CalendarYear', on_delete=models.PROTECT)
    date = models.DateField()
    reference = models.CharField(max_length=20)  # control number/voucher no
    account = models.ForeignKey('chartsofaccounts.ChartsOfAccounts', on_delete=models.PROTECT)
    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_TYPE)
    entry_type = models.CharField(max_length=10, choices=CHOICES)
    description = models.CharField(max_length=255)
    supplier = models.ForeignKey('suppliers.Supplier', on_delete=models.PROTECT, blank=True, null=True)
    customer = models.ForeignKey('customers.Customer', on_delete=models.PROTECT, blank=True, null=True)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.PROTECT, blank=True, null=True)
    check_number = models.CharField(max_length=50, blank=True, null=True)
    bank = models.ForeignKey(Bank, on_delete=models.PROTECT, blank=True, null=True)
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
        return f"{self.reference} - {self.description}"

class PaymentTerm(models.Model):
    transaction = models.ForeignKey(
        JournalEntry,
        on_delete=models.CASCADE,
        related_name='payment_terms'
    )
    due_date = models.DateField()
    amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0.01)])
    remarks = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.transaction.reference or 'Transaction'} - {self.due_date} ({self.amount})"