# views.py
from django.shortcuts import render, get_object_or_404
from .models import Product, Category, ProductImage
from rapidfuzz.fuzz import partial_ratio
from django.core.cache import cache
from django.core.paginator import Paginator


def home_view(request):
    categories = Category.objects.all()  # Fetch all categories
    return render(request, 'store/home.html', {'categories': categories})

    # categories = Category.objects.all()
    # category_products = {}
    
    # for category in categories:
    #     products = Product.objects.filter(category=category)
    #     category_products[category] = products

    # context = {
    #     'categories': categories,
    #     'category_products': category_products
    # }
    # return render(request, 'store/home.html', context)

def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    product_images = ProductImage.objects.filter(product=product)
    context = {
        'product': product,
        'product_images': product_images
    }
    return render(request, 'store/product_detail.html', context)

def product_images(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/product_images.html', {'product': product})

def search_products(request):
    query = request.GET.get('q', '')  # Get the search term from the 'q' parameter in the URL
    
    try:
        products = list(cache.get('products'))
    except:
        products = Product.objects.all()
        cache.set('products', products)

    if query:
        # Create a list to store products with similarity scores
        matched_products = []
        
        for product in products:
            # Calculate similarity scores for the product fields
            name_score = partial_ratio(query, product.name)
            category_score = partial_ratio(query, product.category.name) if product.category else 0
            description_score = partial_ratio(query, product.description)
            
            # Aggregate the highest score
            max_score = max(name_score, category_score, description_score)
            
            # Set a threshold for inclusion in the results (e.g., > 90%)
            if max_score > 90:
                matched_products.append((product, max_score))
        
        # Sort matched products by their similarity score in descending order
        matched_products = sorted(matched_products, key=lambda x: x[1], reverse=True)
        products = [item[0] for item in matched_products]  # Extract only the product objects

        
    # Pagination
    paginator = Paginator(products, 10)  # Show 10 products per page
    page_number = request.GET.get('page')  # Get the current page number from the request
    page_obj = paginator.get_page(page_number)  # Get the products for the current page

    return render(request, 'store/search_results.html', {'page_obj': page_obj, 'query': query})





