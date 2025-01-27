# views.py
from django.shortcuts import render, get_object_or_404
from .models import Product, Category, ProductImage, Brand, Tag
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Q


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
    category_id = product.category.id
    filter_conditions = Q()  # Initialize an empty Q object
    filter_conditions &= Q(category_id=category_id)
    similar_products = Product.objects.filter(filter_conditions).distinct()
    product_images = ProductImage.objects.filter(product=product)
    context = {
        'product': product,
        'product_images': product_images,
        'similar_products': similar_products
    }
    return render(request, 'store/product_detail.html', context)

def product_images(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/product_images.html', {'product': product})
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render
from django.core.cache import cache

def search_products(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category')
    brand_id = request.GET.get('brand')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    discount_type = request.GET.get('discount_type')
    gender_age_group = request.GET.get('gender_age_group')
    tag_ids = request.GET.getlist('tags')
    sort_price = request.GET.get('sort_price', '')


    # Initial queryset for all products, retrieved from cache or database
    products = cache.get_or_set('products', Product.objects.all())

    # Applying filters based on query parameters
    filter_conditions = Q()
    if query:
        filter_conditions &= (Q(name__icontains=query) |
                              Q(description__icontains=query) |
                              Q(tags__name__icontains=query) |
                              Q(brand__name__icontains=query) |
                              Q(category__name__icontains=query) |
                              Q(gender_age_group__icontains=query))

    if category_id:
        filter_conditions &= Q(category_id=category_id)

    if brand_id:
        filter_conditions &= Q(brand_id=brand_id)

    if discount_type:
        filter_conditions &= Q(discount_type=discount_type)

    if gender_age_group:
        filter_conditions &= Q(gender_age_group=gender_age_group)

    if tag_ids:
        filter_conditions &= Q(tags__id__in=tag_ids)
    
    # Apply the filter conditions to the products queryset
    products = products.filter(filter_conditions).distinct()

    # Apply sorting by price if 'sort_price' is provided
    if sort_price == 'low_to_high':
        products = products.order_by('original_price')  # Sort by price ascending
    elif sort_price == 'high_to_low':
        products = products.order_by('-original_price')  # Sort by price descending

    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetch all categories, brands, and tags for filter options
    categories = Category.objects.all()
    brands = Brand.objects.all()
    tags = Tag.objects.all()
    gender_age_group_choices = Product._meta.get_field('gender_age_group').choices
    discount_type_choices = Product._meta.get_field('discount_type').choices

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
        'discount_type': discount_type,  # Add this line
        'discount_type_choices': discount_type_choices,
        'gender_age_group': gender_age_group,
        'gender_age_group_choices': gender_age_group_choices,
        'tag_ids': tag_ids,
        'sort_price': sort_price,  # Add sort_price to context
    }

    return render(request, 'store/search_results.html', context)
