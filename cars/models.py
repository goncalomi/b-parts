from django.db import models
from django.core.validators import RegexValidator


class Customer(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

class LicensePlate(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='license_plates')
    plate_number = models.CharField(
        max_length=8, 
        validators=[
            RegexValidator(
                regex=r'^([0-9]{2}[A-Z]{2}[0-9]{2}|[0-9]{2}-[0-9]{2}-[A-Z]{2})$',
                message='Enter a valid license plate number. Examples: 00AA00 or 00-00-AA'
            )
        ],
        unique=True
    )

    def __str__(self):
        return self.plate_number
    

