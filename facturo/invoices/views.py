from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from invoices.forms import ProductSelectionForm
from invoices.models import Invoice, InvoiceProduct
from listings.models import Product


def invoice_list(request):
    invoices_list = Invoice.objects.all().order_by('-creation_date')
    paginator = Paginator(invoices_list, 8)

    page = request.GET.get('page')
    invoices = paginator.get_page(page)
    return render(request,
                  'invoices/invoice_list.html', {'invoices': invoices})


def invoice_add(request):
    products = Product.objects.all()

    if request.method == 'POST':
        form = ProductSelectionForm(request.POST, products=products)
        if form.is_valid():
            selected = []
            for product in products:
                quantity = form.cleaned_data.get(f'product_{product.id}', 0)
                if quantity and quantity > 0:
                    selected.append({
                        'product': product,
                        'quantity': quantity,
                    })

            request.session['invoice_data'] = [
                {'product_id': item['product'].id, 'quantity': item['quantity']}
                for item in selected
            ]
            return redirect('invoice-confirm')
    else:
        form = ProductSelectionForm(products=products)

    return render(request,
                  'invoices/invoice_add.html', {
                      'products': products,
                      'form': form
                  })


def invoice_confirm(request):
    invoice_data = request.session.get('invoice_data')
    if not invoice_data:
        return redirect('invoice-add')

    products = Product.objects.filter(id__in=[item['product_id'] for item in invoice_data])
    product_map = {p.id: p for p in products}

    selected = []
    total = 0
    for item in invoice_data:
        p = product_map.get(item['product_id'])
        quantity = item['quantity']
        subtotal = p.price * quantity
        selected.append({
            'product': p,
            'quantity': quantity,
            'subtotal': subtotal,
        })
        total += subtotal

    if request.method == 'POST':
        invoice = Invoice.objects.create()
        for article in selected:
            InvoiceProduct.objects.create(
                invoice=invoice,
                product=article['product'],
                quantity=article['quantity'],
            )

        del request.session['invoice_data']

        return redirect('invoice-detail', id=invoice.id)

    return render(request,
                  'invoices/invoice_confirm.html',
                  {'selected': selected, 'total': total}
                  )

def invoice_detail(request, id):
    invoice = get_object_or_404(Invoice, id=id)
    items = invoice.invoiceproduct_set.select_related('product')
    for item in items:
        item.subtotal = item.product.price * item.quantity

    return render(request, 'invoices/invoice_detail.html', {'invoice': invoice, 'items': items})
