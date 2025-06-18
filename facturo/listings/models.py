from django.db import models

class Product(models.Model):
    name = models.fields.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    expiration_date = models.DateField()
    def __str__(self):
        return f"{self.name}"