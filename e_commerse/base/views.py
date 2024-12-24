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
from django.contrib.auth.decorators import login_required
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
        action = request.POST.get('action')  # Distinguish between 'send' and 'resend'

        # Validate phone number
        phone_number = validate_phone_number(phone_number)
        if not phone_number:
            messages.error(request, "Invalid phone number.")
            return render(request, 'register/login_or_signup.html', context)

        # OTP submission
        if otp:
            try:
                otp_record = OTP.objects.get(phone_number=phone_number)
                if otp_record.otp == otp and otp_record.is_valid():
                    # OTP is valid
                    user, created = User.objects.get_or_create(username=phone_number)
                    if created:
                        user.set_password(User.objects.make_random_password())  # Set random password
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

        # Request OTP or Resend OTP
        elif action in ['send', 'resend']:
            otp_record, created = OTP.objects.get_or_create(phone_number=phone_number)

            if action == 'resend' and not otp_record.can_resend():
                if otp_record.resend_count >= 3:
                    messages.error(request, "Maximum OTP resend attempts reached for today.")
                else:
                    messages.error(request, "You can resend OTP only after 1 minute.")
                return render(request, 'register/login_or_signup.html', context)

            # Generate and send OTP
            otp = generate_otp()
            otp_record.otp = otp
            otp_record.created_at = now()
            if action == 'resend':
                otp_record.resend_count += 1
                otp_record.last_resend_at = now()
            otp_record.save()

            # Simulate sending OTP (replace with SMS API in production)
            print(f"""-----------------------------
                  Sending OTP {otp} to {phone_number}
                  -----------------------------""")


           

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




@login_required
def account_page(request):
    user = request.user
    orders = Order.objects.filter(buyer=user)
    purchased_products = orders.filter(status="Delivered")

    return render(request, 'useraccount/user_account.html', {
        'user': user,
        'orders': orders,
        'purchased_products': purchased_products
    })

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