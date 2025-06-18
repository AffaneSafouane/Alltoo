from django.shortcuts import render
from listings.models import Product
from invoices.models import Invoice

def home(request):
    products = Product.objects.all().order_by('-id')[:2]
    invoices = Invoice.objects.all().order_by('creation_date')[:2]
    return render(request,
                  'core/home.html',
                  {'products': products, 'invoices': invoices})