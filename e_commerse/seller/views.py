from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from base.models import Seller
from store.models import Product,Category
from django.contrib.auth.models import User
from django.http import JsonResponse

@login_required
def add_product(request):
    # Check if the user is a seller
    if not hasattr(request.user, 'seller_profile'):
        messages.error(request, "You must be a seller to add products.")
        return redirect('seller_dashboard')

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add_product':
            # Handle adding product
            name = request.POST.get('name')
            category_id = request.POST.get('category')
            price = request.POST.get('price')
            description = request.POST.get('description')
            photo = request.FILES.get('photo')

            if not all([name, category_id, price, description]):
                messages.error(request, "All fields are required.")
            else:
                try:
                    category = Category.objects.get(id=category_id)
                    seller = request.user.seller_profile
                    product = Product.objects.create(
                        seller=seller,
                        name=name,
                        category=category,
                        price=price,
                        description=description,
                        photo=photo
                    )
                    messages.success(request, "Product added successfully!")
                    return redirect('seller_dashboard')
                except Category.DoesNotExist:
                    messages.error(request, "Selected category does not exist.")
        
        elif action == 'add_category':
            # Handle adding category
            category_name = request.POST.get('category-name')
            category_image = request.FILES.get('category-image')

            if not category_name or not category_image:
                return JsonResponse({'error': 'Both name and image are required'}, status=400)
            
            category = Category.objects.create(name=category_name, image=category_image)
            categories = Category.objects.all()
            return render(request, 'seller/add_product.html', {'categories': categories})
            # return JsonResponse({
            #     'id': category.id,
            #     'name': category.name,
            #     'image_url': category.image.url
            # }, status=201)
    
    # Default behavior for GET request
    categories = Category.objects.all()
    return render(request, 'seller/add_product.html', {'categories': categories})


@login_required
def seller_dashboard(request):
    # Check if the user is a seller
    if not hasattr(request.user, 'seller_profile'):
        messages.error(request, "You must be a seller to view this page.")
        return redirect('seller_dashboard')  # Redirect non-sellers elsewhere

    seller = request.user.seller_profile
    products = seller.products.all()  # Access the seller's products using the related_name
    return render(request, 'seller/seller_dashboard.html', {'products': products})
