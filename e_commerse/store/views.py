# views.py
from django.shortcuts import render, get_object_or_404
from .models import Product, Category, ProductImage, Brand, Tag
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
    query = request.GET.get('q', '')
    category_id = request.GET.get('category')
    brand_id = request.GET.get('brand')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    discount_type = request.GET.get('discount_type')
    gender_age_group = request.GET.get('gender_age_group')
    tag_ids = request.GET.getlist('tags')  # Handling multiple tags
    
    # Initial queryset for all products
    products = Product.objects.all()

    print(query,category_id,brand_id,min_price,max_price,discount_type,gender_age_group,tag_ids)
    # Apply search filter
    if query:
        products = products.filter(name__icontains=query)
    
    # Apply category filter
    if category_id:
        products = products.filter(category_id=category_id)

    # Apply brand filter
    if brand_id:
        products = products.filter(brand_id=brand_id)

    # Apply price range filter
    if min_price:
        products = products.filter(original_price__gte=min_price)
    if max_price:
        products = products.filter(original_price__lte=max_price)

    # Apply discount type filter
    if discount_type:
        products = products.filter(discount_type=discount_type)

    # Apply gender/age group filter
    if gender_age_group:
        products = products.filter(gender_age_group=gender_age_group)

    # Apply tags filter
    if tag_ids:
        products = products.filter(tags__id__in=tag_ids).distinct()

    # Pagination
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    gender_age_group_choices = Product._meta.get_field('gender_age_group').choices
    # Fetch all categories, brands, and tags for filter options
    categories = Category.objects.all()
    brands = Brand.objects.all()
    tags = Tag.objects.all()

    context = {
        'page_obj': page_obj,
        'query': query,
        'categories': categories,
        'brands': brands,
        'tags': tags,
        'category_id': category_id,
        'brand_id': brand_id,
        'min_price': min_price,
        'max_price': max_price,
        'discount_type': discount_type,
        'gender_age_group': gender_age_group,
        'gender_age_group_choices': gender_age_group_choices,
        'tag_ids': tag_ids,
    }

    return render(request, 'store/search_results.html', context)