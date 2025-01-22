from django.shortcuts import render,redirect
from .models import CartItem,Cart
from django.shortcuts import get_object_or_404, redirect
from store.models import Product
from orders.models import Order,OrderItems,Address
from django.contrib.auth.decorators import login_required


# Create your views here.
# def cart_view(request):
#     cart = Cart.objects.get(user=request.user)
#     return render(request, 'cart/cart.html', {'cart': cart})

from django.shortcuts import render, redirect
from .models import Cart

def cart_view(request):
    if request.user.is_authenticated:
        # Try to get the cart for the user
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            # If the cart does not exist, create a new one
            cart = Cart.objects.create(user=request.user)

        # Proceed with your logic (e.g., displaying the cart)
        return render(request, 'cart/cart.html', {'cart': cart})
    else:
        # Redirect to login or show an error
        return redirect('login_or_signup_with_otp')


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Check if the product is already in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    return redirect('cart_view')




def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('cart_view')

def update_cart(request, item_id):
    if request.method == "POST":
        cart_item = CartItem.objects.get(id=item_id)
        cart_item.quantity = request.POST.get('quantity', cart_item.quantity)
        cart_item.save()
    return redirect('cart_view')

@login_required
def checkout_view(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all()
    total_price = sum(item.get_total_price() for item in cart_items)
    addresses = Address.objects.filter(user=request.user)

    if request.method == 'POST':
        address_id = request.POST.get('delivery_address')
        if address_id == "new":
            new_address = Address.objects.create(
                user=request.user,
                address=request.POST['address'],
                postal_code=request.POST['postal_code'],
                is_default=request.POST.get('is_default', False) == 'on'
            )
            selected_address = new_address
        else:
            selected_address = Address.objects.get(id=address_id, user=request.user)

        order = Order.objects.create(
            buyer=request.user,
            total_price=total_price,
            delivery_address=selected_address.address
        )

        for item in cart_items:
            OrderItems.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )

        # Clear the cart by deleting all related items
        cart.items.all().delete()

        return redirect('order_confirmation', order_id=order.id)

    return render(request, 'cart/checkout.html', {'addresses': addresses, 'cart_items': cart_items, 'total_price': total_price})
