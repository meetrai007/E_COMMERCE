from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from store.models import Product
from .models import Address, Order  # Assuming the `Order` model is in the `orders` app
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from base.models import Userprofile
from base.forms import UserProfileForm

# @login_required
# @csrf_exempt
# def place_order(request, slug):
#     try:
#         if request.user.IS_seller:
#             messages.info(request,"login as a buyer to place order")
#             return redirect('home')  # Redirect sellers to the homepage
#     except:
#         pass
#     # Fetch the product using slug
#     product = get_object_or_404(Product, slug=slug)
#     user_profile = Userprofile.objects.get(user=request.user)

#     if request.method == 'POST':
#         # Handle address selection or creation
#         address_id = request.POST.get('delivery_address')
#         if address_id == "new":
#             # Create a new address if "Add New Address" is selected
#             new_address = Address.objects.create(
#                 user=request.user,
#                 address_line1=request.POST['address_line1'],
#                 address_line2=request.POST.get('address_line2', ''),
#                 city=request.POST['city'],
#                 state=request.POST['state'],
#                 postal_code=request.POST['postal_code'],
#                 country=request.POST['country'],
#                 is_default=request.POST.get('is_default', False) == 'on'
#             )
#             selected_address = new_address
#         else:
#             # Use the selected existing address
#             selected_address = Address.objects.get(id=address_id, user=request.user)

#         # Fetch the seller associated with the product
#         seller = product.seller

#         # Create the order
#         order = Order.objects.create(
#             buyer=request.user,
#             seller=seller,
#             product=product,
#             quantity=1,  # Adjust as needed
#             total_price=product.price,  # Assuming `price` is a field in Product
#             delivery_address=selected_address.address_line1,  # Store only the line1 for now
#             status='Pending'
#         )
#         product.quantity -= 1
#         product.save()
#         # Redirect to an order success page (or another destination)
#         return redirect('order_success')

#     # Fetch existing addresses for the user
#     addresses = Address.objects.filter(user=request.user)
#     return render(request, 'orders/order_form.html', {'product': product, 'addresses': addresses})

# # orders/views.py
# def order_success(request):
#     return render(request, 'orders/order_success.html')


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItems
from base.forms import AddressForm

@login_required
def buy_now(request, product_id):
    try:
        if request.user.IS_seller:
            messages.info(request,"login as a buyer to place order")
            return redirect('home')
    except:
        pass
    User_profile_form = UserProfileForm
    product = get_object_or_404(Product, id=product_id)
    address = Address.objects.filter(user=request.user)
    
    if request.method == 'POST':
         # Handle address selection or creation
        address_id = request.POST.get('delivery_address')
        if address_id == "new":
            # Create a new address if "Add New Address" is selected
            new_address = Address.objects.create(
                user=request.user,
                address=request.POST['address'],
                postal_code=request.POST['postal_code'],
                is_default=request.POST.get('is_default', False) == 'on')
            selected_address = new_address
        else:
            # Use the selected existing address
            selected_address = Address.objects.get(id=address_id, user=request.user)
            

        # Create the order for the selected product
        order = Order.objects.create(
            buyer=request.user,
            name = request.POST['name'],
            number = request.POST['number'],
            total_price=product.get_discounted_price(),  # Assuming the product price is directly used for the order
            delivery_address=selected_address.address
        )

        # Create an OrderItems for the product
        order_item = OrderItems.objects.create(
            order=order,
            product=product,
            quantity=1  # Assuming user wants to buy one quantity
        )

        # Redirect to an order success page (or another destination)
        return redirect('order_confirmation', order_id=order.id)

    return render(request, 'orders/buy_now.html', {'product': product, 'addresses': address,'User_profile_form':User_profile_form})
@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_confirmation.html', {'order': order})
