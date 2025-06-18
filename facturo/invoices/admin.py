from django.contrib import admin
from .models import Invoice
from .models import InvoiceProduct

class InvoiceProductInline(admin.TabularInline):
    model = InvoiceProduct
    extra = 1
    autocomplete_fields = ['product']

class InvoiceAdmin(admin.ModelAdmin):
    inlines = [InvoiceProductInline]
    list_display = ['id', 'creation_date', 'quantity', 'total']
    list_filter = ['creation_date']

admin.site.register(Invoice, InvoiceAdmin)
