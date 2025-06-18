from datetime import date
from .models import Product
from django import forms

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'expiration_date']
        labels = {
            'name': 'Nom du produit',
            'price': 'Prix (€)',
            'expiration_date': "Date d'expiration",
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'expiration_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                },
                format='%Y-%m-%d',
            ),
        }
        error_messages = {
            'name': {'required': 'Le nom du produit est requis.'},
            'price': {'required': 'Le prix est requis.'},
            'expiration_date': {'required': 'La date d\'expiration est requise.'},
        }

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError('Le prix doit être supérieur à 0.')
        return price

    def clean_expiration_date(self):
        expiration_date = self.cleaned_data['expiration_date']
        if expiration_date < date.today():
            raise forms.ValidationError("La date d'expiration doit être future.")
        return expiration_date