import random
import phonenumbers
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login,authenticate
from orders.models import Order
from seller.models import Seller
from django.contrib import messages
from django.utils.timezone import now
from .models import OTP
from django.core.mail import send_mail  # For simulation; replace with SMS in production


# Helper function to generate OTP
def generate_otp():
    return str(random.randint(100000, 999999))

# Helper function to validate phone number
def validate_phone_number(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number)
        if phonenumbers.is_valid_number(parsed_number):
            return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        else:
            return None
    except phonenumbers.NumberParseException:
        return None

# Login or Signup with OTP
def login_or_signup_with_otp(request):
    context = {}
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        otp = request.POST.get('otp')

        # Validate phone number
        phone_number = validate_phone_number(phone_number)
        if not phone_number:
            messages.error(request, "Invalid phone number.")
            return render(request, 'register/login_or_signup.html', context)

        if otp:  # If OTP is submitted
            try:
                otp_record = OTP.objects.get(phone_number=phone_number)
                if otp_record.otp == otp and otp_record.is_valid():
                    # OTP is valid
                    user, created = User.objects.get_or_create(username=phone_number)
                    if created:
                        user.set_password(User.objects.create_user(None).make_random_password())  # Set random password
                        user.save()
                        messages.success(request, "Account created and logged in successfully.")
                    else:
                        messages.success(request, "Logged in successfully.")

                    auth_login(request, user)
                    otp_record.delete()  # Clear OTP after use
                    return redirect('home')
                else:
                    messages.error(request, "Invalid or expired OTP.")
            except OTP.DoesNotExist:
                messages.error(request, "OTP not found. Please request a new one.")
        else:  # If phone number is submitted to request OTP
            # Generate and send OTP
            otp = generate_otp()
            OTP.objects.update_or_create(phone_number=phone_number, defaults={'otp': otp, 'created_at': now()})

            # Simulate sending OTP (replace this with an SMS API in production)
            print(f"Sending OTP {otp} to {phone_number}")
            # send_mail(
            #     'Your OTP',
            #     f'Your OTP is {otp}',
            #     'noreply@example.com',
            #     ['your_email@example.com'],  # Replace with an SMS gateway
            #     fail_silently=False,
            # )
            messages.info(request, "OTP sent to your phone number.")
            context['otp_sent'] = True
            context['phone_number'] = phone_number

    return render(request, 'register/login_or_signup.html', context)





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


# @login_required
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

# @login_required
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