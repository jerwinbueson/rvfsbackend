from django.db import models




class JournalEntry(models.Model):
    date = models.DateField()
    reference = models.CharField(max_length=20)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.reference} - {self.date}"
    

class GeneralJournal(models.Model):
    entry = models.ForeignKey(JournalEntry, on_delete=models.PROTECT)
    accounts = models.ForeignKey('chartsofaccounts.chartsofaccounts', on_delete=models.PROTECT)
    debit_amount = models.DecimalField(max_digits=30)
    credit_amount = models.DecimalField(max_digits=30)

    def __str__(self):
        return f"{self.reference} - {self.accounts}"
