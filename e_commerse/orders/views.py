from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from store.models import Product
from .models import Address, Order  # Assuming the `Order` model is in the `orders` app
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from base.models import Userprofile

@login_required
@csrf_exempt
def place_order(request, slug):
    try:
        if request.user.IS_seller:
            messages.info(request,"login as a buyer to place order")
            return redirect('home')  # Redirect sellers to the homepage
    except:
        pass
    # Fetch the product using slug
    product = get_object_or_404(Product, slug=slug)
    user_profile = Userprofile.objects.get(user=request.user)

    if request.method == 'POST':
        # Handle address selection or creation
        address_id = request.POST.get('delivery_address')
        if address_id == "new":
            # Create a new address if "Add New Address" is selected
            new_address = Address.objects.create(
                user=request.user,
                address_line1=request.POST['address_line1'],
                address_line2=request.POST.get('address_line2', ''),
                city=request.POST['city'],
                state=request.POST['state'],
                postal_code=request.POST['postal_code'],
                country=request.POST['country'],
                is_default=request.POST.get('is_default', False) == 'on'
            )
            selected_address = new_address
        else:
            # Use the selected existing address
            selected_address = Address.objects.get(id=address_id, user=request.user)

        # Fetch the seller associated with the product
        seller = product.seller

        # Create the order
        order = Order.objects.create(
            buyer=request.user,
            seller=seller,
            product=product,
            quantity=1,  # Adjust as needed
            total_price=product.price,  # Assuming `price` is a field in Product
            delivery_address=selected_address.address_line1,  # Store only the line1 for now
            status='Pending'
        )
        product.quantity -= 1
        product.save()
        # Redirect to an order success page (or another destination)
        return redirect('order_success')

    # Fetch existing addresses for the user
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'orders/order_form.html', {'product': product, 'addresses': addresses})

# orders/views.py
def order_success(request):
    return render(request, 'orders/order_success.html')
