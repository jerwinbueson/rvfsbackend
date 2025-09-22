from django.db import models

class BusinessUnit(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    contact_person = models.ForeignKey('accounts.CustomUser', blank=True, null=True, on_delete=models.PROTECT)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    

    def __str__(self):
        return self.name


class CalendarYear(models.Model):
    business_unit = models.ForeignKey(BusinessUnit, on_delete=models.PROTECT)
    name = models.CharField(max_length=30)
    start_date = models.DateField()
    end_date = models.DateField()
    default = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Only affect records for the same business unit
        if self.default:
            CalendarYear.objects.filter(
                business_unit=self.business_unit
            ).exclude(pk=self.pk).update(default=False)
        elif not CalendarYear.objects.filter(
            business_unit=self.business_unit, default=True
        ).exclude(pk=self.pk).exists():
            self.default = True
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('business_unit', 'name')  
    def __str__(self):
        return f"{self.business_unit} - {self.name}"
