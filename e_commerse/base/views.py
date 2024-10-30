# views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
import os
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.shortcuts import render
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random

# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)  # Log the user in
            messages.success(request, "Logged in successfully!")
            return redirect('home')  # Redirect to the homepage or any other page
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
    
    return render(request,'register/loginpage.html')


def user_account(request):
    return render(request,'try/user_account.html')


# def signup(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']
#         password_confirm = request.POST['password_confirm']

#         # Basic validations
#         if password != password_confirm:
#             messages.error(request, "Passwords do not match.")
#             return redirect('signup')
#         if User.objects.filter(username=username).exists():
#             messages.error(request, "Username already exists.")
#             return redirect('signup')
#         if User.objects.filter(email=email).exists():
#             messages.error(request, "Email already exists.")
#             return redirect('signup')

#         # Create the user
#         user = User.objects.create_user(username=username, email=email, password=password)
#         user.save()
#         messages.success(request, "Account created successfully.")
#         return redirect('login')  # Redirect to login page after successful registration

#     return render(request,'register/signuppage.html')



# Helper function to generate OTP
def generate_otp():
    return str(random.randint(1000, 9999))

# Endpoint to send OTP via email
@csrf_exempt
def send_email_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = generate_otp()
        
        # Send email with the OTP (make sure to set up email backend in settings)
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp}',
            os.environ.get('EMAIL_HOST_USER'),  # Change to your "from" address
            [email],
            fail_silently=False,
        )
        request.session['email_otp'] = otp
        return JsonResponse({'message': 'OTP sent to email'}, status=200)

    return JsonResponse({'error': 'Invalid request'}, status=400)

# Endpoint to validate OTP
@csrf_exempt
def validate_email_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        if otp == request.session.get('email_otp'):
            return JsonResponse({'message': 'OTP verified successfully'}, status=200)
        return JsonResponse({'error': 'Invalid OTP'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)

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


def test_email(request):
    try:
        send_mail(
            'Test Subject',
            'This is a test email.',
            'your_email@outlook.com',  # From address
            ['lllllmeetlllll@gmail.com'],  # To address
            fail_silently=False,
        )
        return HttpResponse("Email sent successfully.")
    except Exception as e:
        return HttpResponse(f"Failed to send email: {str(e)}")