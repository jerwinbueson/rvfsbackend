from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

class JournalEntry(models.Model):
    business_unit = models.ForeignKey('business.BusinessUnit', on_delete=models.PROTECT)
    calendar_year = models.ForeignKey('business.CalendarYear', on_delete=models.PROTECT)
    date = models.DateField()
    reference = models.CharField(max_length=20)  # control number/voucher no
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.reference} - {self.date}"



class JournalLine(models.Model):
    CHOICES = (
        ('Debit', 'Debit'),
        ('Credit', 'Credit'),
    )
    business_unit = models.ForeignKey('business.BusinessUnit', on_delete=models.PROTECT)
    calendar_year = models.ForeignKey('business.CalendarYear', on_delete=models.PROTECT)
    account = models.ForeignKey('chartsofaccounts.ChartsOfAccounts', on_delete=models.PROTECT)
    journal_entry = models.ForeignKey(JournalEntry, on_delete=models.CASCADE, related_name='lines')
    validators=[MinValueValidator(0.01, message="Amount must be greater than 0")],
    type = models.CharField(max_length=10, choices=CHOICES, null=True, blank=True) #Remove this null and blank during production
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0, null=True, blank=True) #Remove this null and blank during production
    particulars = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.journal_entry.reference} - {self.account.name}"

    

# class GeneralJournal(models.Model):
#     business_unit = models.ForeignKey('business.BusinessUnit', on_delete=models.PROTECT)
#     calendar_year = models.ForeignKey('business.CalendarYear', on_delete=models.PROTECT)
#     entry = models.ForeignKey(JournalEntry, on_delete=models.PROTECT)
#     accounts = models.ForeignKey('chartsofaccounts.ChartsOfAccounts', on_delete=models.PROTECT)
#     debit_amount = models.DecimalField(max_digits=30, decimal_places=2, default=0)
#     credit_amount = models.DecimalField(max_digits=30, decimal_places=2, default=0)

#     def __str__(self):
#         return f"{self.reference} - {self.accounts}"


# class CashReceipt(models.Model):
#     business_unit = models.ForeignKey('business.BusinessUnit', on_delete=models.PROTECT)
#     calendar_year = models.ForeignKey('business.CalendarYear', on_delete=models.PROTECT)
#     date = models.DateField()
#     account = models.ForeignKey('chartsofaccounts.ChartsOfAccounts', on_delete=models.PROTECT)
#     description = models.CharField(max_length=255)  # Customer or description
#     reference = models.CharField(max_length=50, blank=True, null=True)
#     cash_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
#     sales_return_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
#     sales_discount_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
#     wht_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
#     sales_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)


#     def __str__(self):
#         return f"CashReceipt {self.reference} - {self.description}"


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
    journal_entry = models.OneToOneField(
        JournalEntry, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='cash_receipt'
    )
    def calculate_sales_amount(self):
        return (
            self.cash_amount - 
            (self.sales_return_amount or 0) - 
            (self.sales_discount_amount or 0) - 
            (self.wht_amount or 0)
        )

    def __str__(self):
        return f"CashReceipt {self.reference} - {self.description}"

    def save(self, *args, **kwargs):
        self.sales_amount = self.calculate_sales_amount()
        is_new = self._state.adding
        super().save(*args, **kwargs)
                
        if is_new:
            self._create_journal_entries()
    
    def _create_journal_entries(self):
        # Create Journal Entry
        journal_entry = JournalEntry.objects.create(
            business_unit=self.business_unit,
            calendar_year=self.calendar_year,
            date=self.date,
            reference=f"{self.reference or self.id}",
            description=f"Cash receipt: {self.description}",
        )
        
        # Create Debit entry (Cash)
        if self.cash_amount > 0:
            JournalLine.objects.create(
                business_unit=self.business_unit,
                calendar_year=self.calendar_year,
                account=self.account,  # This should be the cash account
                journal_entry=journal_entry,
                type='Debit',
                amount=self.cash_amount,
                particulars=f"Cash receipt from {self.description}"
            )
        
        # Create Credit entry (Sales)
        if self.sales_amount > 0:
            # You might want to get the sales account from settings or another source
            sales_account = self.account  # Replace with actual sales account logic
            JournalLine.objects.create(
                business_unit=self.business_unit,
                calendar_year=self.calendar_year,
                account=sales_account,
                journal_entry=journal_entry,
                type='Credit',
                amount=self.sales_amount,
                particulars=f"Sales from {self.description}"
            )
        
        # Link the journal entry to this cash receipt
        self.journal_entry = journal_entry
        self.save(update_fields=['journal_entry'])





class CashDisbursement(models.Model):
    business_unit = models.ForeignKey('business.BusinessUnit', on_delete=models.PROTECT, null=True, blank=True)
    calendar_year = models.ForeignKey('business.CalendarYear', on_delete=models.PROTECT, null=True, blank=True)
    account = models.ForeignKey('chartsofaccounts.ChartsOfAccounts', on_delete=models.PROTECT, related_name='cash_disbursements', null=True, blank=True)
    date = models.DateField()
    description = models.CharField(max_length=255)  # Supplier or description
    reference = models.CharField(max_length=50, blank=True, null=True)
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

    def _create_journal_entries(self):
        journal_entry = JournalEntry.objects.create(
            date=self.date,
            reference=f"{self.invoice_number or self.id}",
            description=f"Cash disbursement: {self.description}",
        )

        # Debit Purchase / Expense account
        purchase_account = ...  # get from settings or related ChartOfAccounts
        net_purchase = self.purchase_amount - self.purchase_return_amount - self.purchase_discount_amount
        if net_purchase > 0:
            JournalLine.objects.create(
                journal_entry=journal_entry,
                account=purchase_account,
                type='Debit',
                amount=net_purchase,
                particulars=f"Payment to supplier {self.description}"
            )

        # Debit Purchase Returns / Discounts if any
        if self.purchase_return_amount > 0:
            returns_account = ...
            JournalLine.objects.create(
                journal_entry=journal_entry,
                account=returns_account,
                type='Credit',  # contra-purchase
                amount=self.purchase_return_amount,
                particulars=f"Purchase return from {self.description}"
            )

        if self.purchase_discount_amount > 0:
            discount_account = ...
            JournalLine.objects.create(
                journal_entry=journal_entry,
                account=discount_account,
                type='Credit',
                amount=self.purchase_discount_amount,
                particulars=f"Purchase discount from {self.description}"
            )

        # Debit WHT if any
        if self.wht_amount > 0:
            wht_account = ...
            JournalLine.objects.create(
                journal_entry=journal_entry,
                account=wht_account,
                type='Credit',
                amount=self.wht_amount,
                particulars=f"WHT on payment to {self.description}"
            )

        # Credit Cash
        if self.cash_amount > 0:
            cash_account = ...
            JournalLine.objects.create(
                journal_entry=journal_entry,
                account=cash_account,
                type='Credit',
                amount=self.cash_amount,
                particulars=f"Cash payment to {self.description}"
            )

        self.journal_entry = journal_entry
        self.save(update_fields=['journal_entry'])


    
class Sales(models.Model):
    journal_entry = models.OneToOneField(JournalEntry, on_delete=models.CASCADE, related_name='sale')
    invoice_number = models.CharField(max_length=50)
    customer = models.CharField(max_length=255)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    terms = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Sale {self.invoice_number} - {self.customer}"
