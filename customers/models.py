from django.db import models

class Customer(models.Model):
    CHOICES = [
        ('Individual', 'Individual'),
        ('Business', 'Business'),
    ]

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=CHOICES)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    
    def __str__(self):
        return self.name
        