from django import forms


class ProductSelectionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        products = kwargs.pop('products')
        super().__init__(*args, **kwargs)

        if products:
            self.products = products
            self.product_rows = []
            for product in products:
                field_name = f'product_{product.id}'
                self.fields[field_name] = forms.IntegerField(
                    label=product.name,
                    min_value=0,
                    initial=0,
                    required=False,
                    widget=forms.NumberInput(attrs={
                        'class': 'form-control',
                        'style': 'width: 100px; display: inline-block; margin-left: 10px;',
                    }),
                )
                self.product_rows.append({
                    'field': self[field_name],
                    'product': product,
                })

    def clean(self):
        cleaned_data = super().clean()

        has_quantity = False
        for product in self.products:
            qty = cleaned_data.get(f'product_{product.id}')
            if qty and qty > 0:
                has_quantity = True
                break

        if not has_quantity:
            raise forms.ValidationError('Veuillez sélectionner au moins un produit.')

        return cleaned_data
