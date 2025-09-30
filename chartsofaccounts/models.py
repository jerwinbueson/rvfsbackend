from django.db import models


class AccountType(models.Model):
    business_unit = models.ForeignKey('business.BusinessUnit', on_delete=models.PROTECT, blank=True, null=True) #Remove this blank and null during production
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class CashFlowType(models.Model):
    business_unit = models.ForeignKey('business.BusinessUnit', on_delete=models.PROTECT, blank=True, null=True) #Remove this blank and null during production
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class ChartsOfAccounts(models.Model):
    business_unit = models.ForeignKey('business.BusinessUnit', on_delete=models.PROTECT, blank=True, null=True) #Remove this blank and null during production
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    type = models.ForeignKey(AccountType, on_delete=models.PROTECT)
    cash_flow_type = models.ForeignKey(CashFlowType, on_delete=models.PROTECT)
    description = models.CharField(max_length=150)

    class Meta:
        unique_together = ('business_unit', 'code', 'name')

    def __str__(self):
        return self.name

