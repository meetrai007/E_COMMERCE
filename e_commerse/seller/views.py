from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from seller.models import Seller
from store.models import Product,Category
from django.contrib.auth.models import User
from django.http import JsonResponse
from orders.models import Order

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



def seller_dashboard(request):
    seller_id = request.session.get('seller_id')
    if not seller_id:
        return redirect('seller_login')

    seller = Seller.objects.get(seller_id=seller_id)
    return render(request, 'seller/seller_dashboard.html', {'seller': seller})

def seller_logout(request):
    request.session.flush()  # Clear all session data
    return redirect('seller_login')

def seller_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        if Seller.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        else:
            seller = Seller.objects.create(
                username=username,
                email=email,
                owner_name=request.POST['owner_name'],
                shop_name=request.POST['shop_name'],
                shop_address=request.POST['shop_address'],
                phone=request.POST['phone']
            )
            seller.set_password(password)  # Save the hashed password
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('seller_login')

    return render(request, 'seller/seller_register.html')



def seller_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            seller = Seller.objects.get(username=username)
            if seller.check_password(password):
                # Save the seller's ID in the session
                request.session['seller_id'] = seller.seller_id
                return redirect('seller_dashboard')
            else:
                messages.error(request, 'Invalid password.')
        except Seller.DoesNotExist:
            messages.error(request, 'Seller not found.')

    return render(request, 'seller/seller_login.html')
