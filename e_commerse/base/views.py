# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login as auth_login,authenticate
from django.contrib.auth.decorators import login_required
from seller.models import Seller
from orders.models import Order

# Create your views here.
def login(request):
    """
    Handles the login form submission and logs the user in.
    """
    if request.method == 'POST':
        # Get the username and password from the form
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log the user in
            auth_login(request, user)
            # Show a success message
            messages.success(request, "Logged in successfully!")
            # Redirect to the homepage or any other page
            return redirect('home')
        else:
            # Show an error message
            messages.error(request, "Invalid username or password.")
            # Redirect to the login page
            return redirect('login')
    
    # Render the login page if the request is not a POST
    return render(request, 'register/loginpage.html')


@login_required
def account_page(request):
    user = request.user
    orders = Order.objects.filter(buyer=user)
    purchased_products = orders.filter(status="Delivered")

    return render(request, 'useraccount/user_account.html', {
        'orders': orders,
        'purchased_products': purchased_products
    })

# Signup view
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        email_otp = request.POST.get('emailOtp')

        # Validate OTP
        if email_otp != request.session.get('email_otp'):
            messages.error(request, "Invalid OTP.")
            return redirect('signup')

        # Validate passwords match
        if password != password_confirm:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        # Check if user or email already exists
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            messages.error(request, "Username or email already exists.")
            return redirect('signup')

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Account created successfully.")
        return redirect('login')

    return render(request, 'register/signuppage.html')

@login_required
def become_seller(request):
    if hasattr(request.user, 'seller_profile'):
        messages.info(request, "You are already registered as a seller.")
        return redirect('home')  # Redirect to a dashboard or relevant page

    if request.method == 'POST':
        owner_name = request.POST.get('owner_name')
        shop_name = request.POST.get('shop_name')
        shop_address = request.POST.get('shop_address')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        if owner_name and shop_name and shop_address and email and phone:
            seller = Seller.objects.create(
                user=request.user,
                owner_name=owner_name,
                shop_name=shop_name,
                shop_address=shop_address,
                email=email,
                phone=phone
            )
            messages.success(request, "You are now a seller!")
            return redirect('home')  # Redirect to a dashboard or relevant page
        else:
            messages.error(request, "All fields are required.")

    return render(request, 'register/become_seller.html')