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
    name = models.CharField(max_length=30)
    start_date = models.DateField()
    end_date = models.DateField()