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
    # FIX 1: Moved validators into the amount field definition
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

    # FIX 2: Improved save method logic for creating and linking entries
    def save(self, *args, **kwargs):
        self.sales_amount = self.calculate_sales_amount()
        is_new = self._state.adding
        super().save(*args, **kwargs)

        if is_new and not self.journal_entry:
            try:
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
                    # For now, using the same account field (which should be the cash account)
                    # This needs correction: Credit Sales, Debit Cash
                    # The logic here assumes 'self.account' is the cash account for the debit.
                    # You need to fetch the appropriate SALES account for the credit.
                    sales_account = self.account # <<< REPLACE WITH ACTUAL SALES ACCOUNT LOGIC >>>
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
                # Use update_fields to avoid calling save signals again unnecessarily
                # and only save the specific field.
                super().save(update_fields=['journal_entry'])

            except Exception as e:
                # Handle potential errors during journal creation
                # e.g., log the error, raise a ValidationError, or delete the half-created entries
                print(f"Error creating journal entries for CashReceipt {self.id}: {e}")
                # Optionally, raise an error to prevent saving the CashReceipt without journals
                # raise ValidationError("Could not create corresponding journal entries.") from e


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
    disbursement_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    journal_entry = models.OneToOneField(
        JournalEntry,
        on_delete=models.CASCADE,
        related_name='cash_disbursement',
        null=True,
        blank=True
    )
    def calculate_disbursement_amount(self):
        return (
            self.cash_amount - 
            (self.purchase_return_amount or 0) -
            (self.purchase_discount_amount or 0) -
            (self.wht_amount or 0)
        )
    # FIX 3: Corrected __str__ method
    def __str__(self):
        return f"CashDisbursement {self.reference} - {self.description}"

    # FIX 4: Implemented save method to call journal creation
    def save(self, *args, **kwargs):
        self.disbursement_amount = self.calculate_disbursement_amount()
        # Add logic here if you need to calculate purchase_amount like sales_amount in CashReceipt
        # e.g., self.purchase_amount = self.cash_amount + self.purchase_return_amount + self.purchase_discount_amount - self.wht_amount
        # Or ensure it's set correctly before saving.
        is_new = self._state.adding
        super().save(*args, **kwargs)

        if is_new and not self.journal_entry:
             try:
                self._create_journal_entries()
             except Exception as e:
                print(f"Error creating journal entries for CashDisbursement {self.id}: {e}")
                # Decide how to handle errors: raise ValidationError or just log.

    # FIX 4 & 5: Completed _create_journal_entries method
    def _create_journal_entries(self):
        # Ensure required fields are set before creating journals
        if not self.business_unit or not self.calendar_year:
             raise ValidationError("Business Unit and Calendar Year are required before creating journal entries.")

        # Get or determine account ids
        # <<< YOU MUST IMPLEMENT THIS LOGIC >>>
        # Example (assuming you have a way to get these accounts):
        # purchase_account = ChartsOfAccounts.objects.get(code='5000') # Example Purchase Account
        # cash_account = ChartsOfAccounts.objects.get(code='1000')     # Example Cash Account
        # purchase_returns_account = ChartsOfAccounts.objects.get(code='5100') # Example Purchase Returns Account
        # purchase_discounts_account = ChartsOfAccounts.objects.get(code='5200') # Example Purchase Discounts Account
        # wht_payable_account = ChartsOfAccounts.objects.get(code='2200') # Example WHT Payable Account
        purchase_account = self.account # <<< REPLACE WITH ACTUAL PURCHASE ACCOUNT LOGIC >>>
        cash_account = self.account     # <<< REPLACE WITH ACTUAL CASH ACCOUNT LOGIC >>>
        purchase_returns_account = None # <<< REPLACE WITH ACTUAL RETURNS ACCOUNT LOGIC >>>
        purchase_discounts_account = None # <<< REPLACE WITH ACTUAL DISCOUNTS ACCOUNT LOGIC >>>
        wht_payable_account = None # <<< REPLACE WITH ACTUAL WHT ACCOUNT LOGIC >>>

        if not purchase_account or not cash_account:
             raise ValidationError("Cannot determine necessary accounts (Purchase, Cash) for journal entry.")

        # Calculate net purchase amount
        net_purchase = self.purchase_amount - (self.purchase_return_amount or 0) - (self.purchase_discount_amount or 0)


        journal_entry = JournalEntry.objects.create(
            business_unit=self.business_unit,
            calendar_year=self.calendar_year, # Added missing fields
            date=self.date,
            reference=f"{self.reference or self.id}", # Use reference or ID
            description=f"Cash disbursement: {self.description}",
        )

        # Debit Purchase / Expense account
        if net_purchase > 0:
            JournalLine.objects.create(
                business_unit=self.business_unit,
                calendar_year=self.calendar_year, # Added missing fields
                journal_entry=journal_entry,
                account=purchase_account,
                type='Debit',
                amount=net_purchase,
                particulars=f"Payment to supplier {self.description}"
            )

        # Credit Purchase Returns / Discounts if any (Contra-Purchase accounts)
        if self.purchase_return_amount and self.purchase_return_amount > 0 and purchase_returns_account:
            JournalLine.objects.create(
                 business_unit=self.business_unit,
                calendar_year=self.calendar_year, # Added missing fields
                journal_entry=journal_entry,
                account=purchase_returns_account, # Use specific returns account
                type='Credit',  # contra-purchase
                amount=self.purchase_return_amount,
                particulars=f"Purchase return from {self.description}"
            )

        if self.purchase_discount_amount and self.purchase_discount_amount > 0 and purchase_discounts_account:
            JournalLine.objects.create(
                business_unit=self.business_unit,
                calendar_year=self.calendar_year, # Added missing fields
                journal_entry=journal_entry,
                account=purchase_discounts_account, # Use specific discount account
                type='Credit',
                amount=self.purchase_discount_amount,
                particulars=f"Purchase discount from {self.description}"
            )

        # Credit WHT if any (WHT Payable account)
        if self.wht_amount and self.wht_amount > 0 and wht_payable_account:
            JournalLine.objects.create(
                business_unit=self.business_unit,
                calendar_year=self.calendar_year, # Added missing fields
                journal_entry=journal_entry,
                account=wht_payable_account, # Use specific WHT account
                type='Credit',
                amount=self.wht_amount,
                particulars=f"WHT on payment to {self.description}"
            )

        # Credit Cash
        if self.cash_amount and self.cash_amount > 0:
            JournalLine.objects.create(
                business_unit=self.business_unit,
                calendar_year=self.calendar_year, # Added missing fields
                journal_entry=journal_entry,
                account=cash_account, # Use specific cash account
                type='Credit',
                amount=self.cash_amount,
                particulars=f"Cash payment to {self.description}"
            )

        # Link the journal entry to this cash disbursement
        self.journal_entry = journal_entry
        # Use the parent save to avoid re-triggering _create_journal_entries
        super(CashDisbursement, self).save(update_fields=['journal_entry'])


class Sales(models.Model):
    journal_entry = models.OneToOneField(JournalEntry, on_delete=models.CASCADE, related_name='sale')
    invoice_number = models.CharField(max_length=50)
    customer = models.CharField(max_length=255)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    terms = models.CharField(max_length=100, blank=True, null=True)

    # FIX 5: Corrected __str__ method typo
    def __str__(self):
        return f"Sale {self.invoice_number} - {self.customer}"