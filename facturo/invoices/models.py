from django.db import models

from listings.models import Product

class Invoice(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, blank=True, through='InvoiceProduct')

    @property
    def quantity(self):
        return sum(ip.quantity for ip in self.invoiceproduct_set.all())

    @property
    def total(self):
        return sum(ip.product.price * ip.quantity for ip in self.invoiceproduct_set.all())

class InvoiceProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()