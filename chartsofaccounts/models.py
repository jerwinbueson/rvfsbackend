from django.db import models


class AccountType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class CashFlowType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class ChartsOfAccounts(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    type = models.ForeignKey(AccountType, on_delete=models.PROTECT)
    cash_flow_type = models.ForeignKey(CashFlowType, on_delete=models.PROTECT)
    description = models.CharField(max_length=150)

    def __str__(self):
        return self.name