from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CashDisbursement, JournalEntry

@receiver(post_save, sender=CashDisbursement)
def create_journal_entry_for_cash_disbursement(sender, instance, created, **kwargs):
    if created:
        # Create a journal entry for the cash disbursement
        journal_entry = JournalEntry.objects.create(
            business_unit=instance.business_unit,
            calendar_year=instance.calendar_year,
            date=instance.date,
            reference=instance.reference,
            account=instance.account,
            transaction_type=instance.transaction_type,
            amount=instance.cash_amount,
            particulars=instance.description
        )
        # Update the cash disbursement with the journal entry
        instance.journal_entry = journal_entry
        instance.save(update_fields=['journal_entry'])