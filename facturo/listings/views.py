from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ProductForm
from .models import Product


def product_list(request):
    products_list = Product.objects.all().order_by('-id')
    paginator= Paginator(products_list, 10)

    page = request.GET.get('page')
    products = paginator.get_page(page)
    return render(request, 
                  'listings/product_list.html',
                  {'products': products})

def product_add(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre produit a bien été enregistré.')
            return redirect('product-list')
    else:
        form = ProductForm()

    return render(request,
                      'listings/product_add.html',
                      {'form': form})

def product_update(request, id):
    product = Product.objects.get(id=id)

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre produit a bien été mis à jour.')
            return redirect('product-list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'listings/product_update.html',
                  {'form': form})

def product_delete(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == "POST":
        product.delete()
        messages.success(request, f'Le produit "{product.name}" a bien été supprime.')
        return redirect('product-list')

    return render(request,
                  'listings/product_delete.html',
                  {'product': product})