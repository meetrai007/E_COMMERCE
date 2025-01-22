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
    tag_ids = request.GET.getlist('tags')

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

    if min_price:
        try:
            min_price = float(min_price)
            filter_conditions &= Q(original_price__gte=min_price)
        except ValueError:
            pass  # Handle invalid min_price input gracefully

    if max_price:
        try:
            max_price = float(max_price)
            filter_conditions &= Q(original_price__lte=max_price)
        except ValueError:
            pass  # Handle invalid max_price input gracefully

    if discount_type:
        filter_conditions &= Q(discount_type=discount_type)

    if gender_age_group:
        filter_conditions &= Q(gender_age_group=gender_age_group)

    if tag_ids:
        filter_conditions &= Q(tags__id__in=tag_ids)

    products = products.filter(filter_conditions).distinct()

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
    }

    return render(request, 'store/search_results.html', context)
