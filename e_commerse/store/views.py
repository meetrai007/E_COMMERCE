# views.py
from django.shortcuts import render
from .models import Category, Product
from django.shortcuts import render, get_object_or_404
from .models import Product
from django.db.models import Q

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


def search_products(request):
    query = request.GET.get('q', '')  # Get the search term from the 'q' parameter in the URL
    products = Product.objects.filter(
    Q(name__icontains=query) |
    Q(category__name__icontains=query) |  # Assuming `category` is a ForeignKey to a Category model with a `name` field
    Q(description__icontains=query)
) if query else Product.objects.all()
    
    return render(request, 'store/search_results.html', {'products': products, 'query': query})



