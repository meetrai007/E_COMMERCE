from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from base.models import Seller
from store.models import Product,Category
from django.contrib.auth.models import User

@login_required
def add_product(request):
    # Check if the user is a seller
    if not hasattr(request.user, 'seller_profile'):
        messages.error(request, "You must be a seller to add products.")
        return redirect('seller_dashboard')  # Replace with your dashboard or home page

    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        description = request.POST.get('description')
        photo = request.FILES.get('photo')

        # Validation
        if not all([name, category_id, price, description]):
            messages.error(request, "All fields are required.")
        else:
            # Create product
            category = Category.objects.get(id=category_id)
            seller = request.user.seller_profile  # Get the logged-in user's seller profile
            product = Product.objects.create(
                seller=seller,
                name=name,
                category=category,
                price=price,
                description=description,
                photo=photo
            )
            messages.success(request, "Product added successfully!")
            return redirect('seller_dashboard')  # Replace with your seller dashboard page

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
