# views.py
from django.shortcuts import render
from .models import Category, Product
from django.shortcuts import render, get_object_or_404
from .models import Product

def home_view(request):
    categories = Category.objects.all()
    category_products = {}
    
    for category in categories:
        products = Product.objects.filter(category=category)
        category_products[category] = products

    context = {
        'categories': categories,
        'category_products': category_products
    }
    return render(request, 'store/home.html', context)


def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    context = {
        'product': product
    }
    return render(request, 'store/product_detail.html', context)
