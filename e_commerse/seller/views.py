from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from seller.models import Seller
from store.models import Product,Category
from django.contrib.auth.models import User
from django.http import JsonResponse
from orders.models import Order
from django.contrib.auth import authenticate, login

@login_required(login_url='/seller/login/')
def add_product(request):
    

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
                    seller = Seller.objects.get(username=request.user.username)
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





@login_required(login_url='/seller/login/')
def seller_dashboard(request):
    sellername = request.user.username
    seller_id = request.user.seller_id

    # Fetch products and orders
    products = Product.objects.filter(seller=seller_id)
    orders = Order.objects.filter(product__seller=seller_id)
    categories = Category.objects.all()  # Get all categories for dropdown

    # Handle Add Product logic
    if request.method == 'POST' and request.POST.get('action') == 'add_product':
        name = request.POST['name']
        category_id = request.POST['category']
        price = request.POST['price']
        description = request.POST['description']
        photo = request.FILES.get('photo')

        category = Category.objects.get(id=category_id)
        Product.objects.create(
            name=name,
            category=category,
            price=price,
            description=description,
            photo=photo,
            seller=request.user
        )
        return redirect('seller_dashboard')

    context = {
        'sellername': sellername,
        'products': products,
        'orders': orders,
        'categories': categories,
        'seller': request.user
    }
    return render(request, 'seller/seller_dashboard.html', context)
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

        # Authenticate the seller using the custom backend
        seller = authenticate(request, username=username, password=password)

        if seller is not None:
            login(request, seller)  # Logs in the seller
            request.session['is_seller'] = True
            return redirect('home')  # Redirect to a dashboard or test page
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'seller/seller_login.html')


def remove_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('seller_dashboard')  # Redirect back to the view products page

def edit_product(request, product_id):
    # Get the product to edit
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()  # Assuming you have a Category model

    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        description = request.POST.get('description')
        photo = request.FILES.get('photo')

        # Validate the form fields (you can add more validations if needed)
        if not name or not price or not description:
            # Handle the case where required fields are missing
            error_message = "Please fill in all required fields."
            return render(request, 'seller/edit_product.html', {
                'product': product,
                'categories': categories,
                'error_message': error_message,
            })

        # Get the category instance
        category = get_object_or_404(Category, id=category_id)

        # Update the product instance
        product.name = name
        product.category = category
        product.price = price
        product.description = description
        if photo:
            product.photo = photo  # Update the photo if a new one is uploaded

        product.save()  # Save the updated product

        return redirect('seller_dashboard')  # Redirect to the product listing page

    return render(request, 'seller/edit_product.html', {
        'product': product,
        'categories': categories,
    })