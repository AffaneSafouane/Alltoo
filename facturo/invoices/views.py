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
    all_products = Product.objects.all()
    paginator = Paginator(all_products, 8)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    products = page_obj.object_list
    
    session_key = 'invoice_selection'
    stored_data = request.session.get(session_key, {})

    if request.method == 'POST':
        form = ProductSelectionForm(request.POST, products=products, post_data=request.POST)
        if form.is_valid():
            updated_data = stored_data.copy()
            for product in products:
                quantity = form.cleaned_data.get(f'product_{product.id}', 0)
                if quantity and quantity > 0:
                    updated_data[str(product.id)] = quantity
                elif str(product.id) in updated_data:
                    del updated_data[str(product.id)]

            request.session[session_key] = updated_data
            
            if 'next' in request.POST:
                next_page = int(page_number) + 1
                if next_page <= paginator.num_pages:
                    return redirect(f'{request.path}?page={next_page}')
            elif 'prev' in request.POST:
                prev_page = int(page_number) - 1
                if prev_page >= 1:
                    return redirect(f'{request.path}?page={prev_page}')
            elif 'cancel' in request.POST:
                request.session.pop('invoice_selection', None)
                return redirect('home') 
            elif 'order' in request.POST:
                return redirect('invoice-confirm')
    else:
        initial = {}
        for product in products:
            product_id = str(product.id)
            if product_id in stored_data:
                initial[f'product_{product.id}'] = stored_data[product_id]
        form = ProductSelectionForm(products=products, initial=initial)

    return render(request,
                  'invoices/invoice_add.html', {
                      'products': products,
                      'form': form,
                      'page_obj':page_obj
                  })


def invoice_confirm(request):
    invoice_data = request.session.get('invoice_selection')
    if not invoice_data:
        return redirect('invoice-add')

    product_ids = [int(pid) for pid in invoice_data.keys()]
    products = Product.objects.filter(id__in=product_ids)
    product_map = {p.id: p for p in products}

    selected = []
    total = 0
    
    for pid_str, quantity in invoice_data.items():
        pid = int(pid_str)
        product = product_map.get(pid)
        if product:
            subtotal = product.price * int(quantity)
            selected.append({
                'product': product,
                'quantity': int(quantity),
                'subtotal': subtotal,
            })
            total += subtotal

    if request.method == 'POST':
        if 'cancel' in request.POST:
            request.session.pop('invoice_selection', None)
            return redirect('home') 
        if 'confirm' in request.POST:
            invoice = Invoice.objects.create()
            for article in selected:
                InvoiceProduct.objects.create(
                    invoice=invoice,
                    product=article['product'],
                    quantity=article['quantity'],
                )

            request.session.pop('invoice_selection', None)

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
