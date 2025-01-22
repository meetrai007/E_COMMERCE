from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from seller.models import Seller
from store.models import Product, Category,ProductImage, Brand
from orders.models import Order, OrderItems
from django.contrib.auth import authenticate, login
from django.core.cache import cache
from decimal import Decimal

@login_required(login_url="/seller/login/")
def seller_dashboard(request):
    sellername = request.user.username
    seller_id = request.user.seller_id

    # Fetch products and orders
    products = Product.objects.filter(seller=seller_id)
    categories = Category.objects.all()  # Get all categories for dropdown
    brands = Brand.objects.all()
    orders = OrderItems.objects.filter(product__seller=seller_id)

    # Handle Add Product logic
    if request.method == "POST":
        name = request.POST["name"]
        category_id = request.POST["category"]
        original_price = request.POST["original_price"]
        discount_type = request.POST["discount_type"]
        discount_value = request.POST["discount_value"]
        quantity = request.POST["quantity"]
        description = request.POST["description"]
        brand = request.POST["brand"]
        photos = request.FILES.getlist("photos")  # Get multiple files uploaded

        category = Category.objects.get(id=category_id)
        brand = Brand.objects.get(id=brand)
        
        # Create the product
        product = Product.objects.create(
            name=name,
            category=category,
            original_price=original_price,
            discount_type=discount_type,
            discount_value=discount_value,
            quantity=quantity,
            brand=brand,
            description=description,
            seller=request.user,
        )
        
        # Save each photo as a ProductImage
        for photo in photos:
            ProductImage.objects.create(product=product, image=photo)

        # Optionally, update the cache (although this isn't strictly necessary here)
        cache.set("products", products)
        
        return redirect("seller_dashboard")

    context = {
        "sellername": sellername,
        "products": products,
        "orders": orders,
        "categories": categories,
        "seller": request.user,
        "brands": brands,
        # "buyer_profile": buyer_profile,
    }
    return render(request, "seller/seller_dashboard.html", context)

def seller_logout(request):
    request.session.flush()  # Clear all session data
    return redirect("seller_login")


def seller_register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]

        if Seller.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
            seller = Seller.objects.create(
                username=username,
                email=email,
                owner_name=request.POST["owner_name"],
                shop_name=request.POST["shop_name"],
                shop_address=request.POST["shop_address"],
                phone=request.POST["phone"],
            )
            seller.set_password(password)  # Save the hashed password
            messages.success(request, "Registration successful. You can now log in.")
            return redirect("seller_login")

    return render(request, "seller/seller_register.html")


def seller_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # Authenticate the seller using the custom backend
        seller = authenticate(request, username=username, password=password) 

        if seller is not None:
            login(request, seller)  # Logs in the seller
            request.session["not_admin"] = True  # Set a custom session variable
            messages.success(request, "Login successful as a seller.")
            return redirect("home")  # Redirect to a dashboard or test page
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "seller/seller_login.html")


def remove_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect("seller_dashboard")  # Redirect back to the view products page
def remove_product_image(request, image_id):
    image = get_object_or_404(ProductImage, id=image_id)
    image.delete()
    return redirect("seller_dashboard")  # Redirect back to the view products page

def edit_product(request, product_id):
    # Get the product to edit
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()  # Get all categories
    brands = Brand.objects.all()

    if request.method == "POST":
        # Get form data
        name = request.POST.get("name")
        category_id = request.POST.get("category")
        original_price = request.POST.get("original_price")
        discount_type = request.POST.get("discount_type")
        discount_value = request.POST.get("discount_value")
        quantity = request.POST.get("quantity")
        description = request.POST.get("description")
        gender = request.POST.get("gender")
        brand = request.POST.get("brand")
        new_photos = request.FILES.getlist("photos")  # Get multiple new images uploaded

        # Validate the form fields
        if not name or not original_price or not description or not quantity or not gender:
            messages.error(request, "All fields are required.")
            return render(
                request,
                "seller/edit_product.html",
                {
                    "product": product,
                    "categories": categories,
                    "brands": brands,
                },
            )

        # Get the selected category
        category = get_object_or_404(Category, id=category_id)

        # Update product details
        product.name = name
        product.category = category
        product.original_price = original_price
        product.discount_type = discount_type
        product.discount_value = discount_value
        product.quantity = quantity
        product.description = description
        product.gender_age_group = gender

        # Save the updated product
        product.save()

        # Handle new photos (multiple uploads)
        if new_photos:
            # Create ProductImage instances for new photos
            for photo in new_photos:
                ProductImage.objects.create(product=product, image=photo)

        # Optionally, clear the cache or update the cache with new data
        cache.set("products", Product.objects.all())

        messages.success(request, "Product updated successfully.")
        return redirect("seller_dashboard")  # Redirect to the seller dashboard after updating

    # Return the edit product page with the existing product data
    return render(
        request,
        "seller/edit_product.html",
        {
            "product": product,
            "categories": categories,
            "brands": brands,
        },
    )




# def apply_discount(request):
#     if request.method == 'POST':
#         # Get the discount percentage from the POST request
#         discount_percentage = request.POST.get('discount_percentage')

#         # Validate the discount percentage
#         if not discount_percentage or not discount_percentage.isdigit():
#             messages.error(request, 'Invalid discount percentage!')
#             return redirect('apply_discount')  # Redirect to the same page with an error message
        
#         discount_percentage = float(discount_percentage)
#         if not (1 <= discount_percentage <= 100):
#             messages.error(request, 'Discount percentage must be between 1 and 100!')
#             return redirect('apply_discount')

#         # Get the selected product IDs from the POST request
#         selected_products = request.POST.getlist('products')

#         if not selected_products:
#             messages.error(request, 'No products selected for discount!')
#             return redirect('apply_discount')

#         # Apply discount to selected products
#         for product_id in selected_products:
#             try:
#                 product = Product.objects.get(id=product_id)
#                 original_price = product.price
#                 discounted_price = original_price - (original_price * discount_percentage / 100)
#                 product.price = discounted_price
#                 product.save()
#             except Product.DoesNotExist:
#                 messages.error(request, f'Product with ID {product_id} does not exist.')

#         messages.success(request, f'Discount of {discount_percentage}% applied successfully to selected products!')
#         return redirect('seller_dashboard')  # Redirect back to the seller's dashboard or another appropriate page

#     # Render the form with existing products for selecting a discount
#     products = Product.objects.all()  # You can filter this list if needed
#     return render(request, 'your_template.html', {'products': products})

# def apply_discount(request):
#     if request.method == 'POST':
#         discount_percentage = Decimal(request.POST.get('discount_percentage'))  # Convert to Decimal
#         selected_products = request.POST.getlist('products')

#         for product_id in selected_products:
#             product = Product.objects.get(id=product_id)
#             original_price = product.price  # This should already be a Decimal
#             discounted_price = original_price - (original_price * discount_percentage / 100)  # Corrected calculation
#             product.price = discounted_price
#             product.save()

#         # Redirect after success
#         return redirect('discount_success')  # Replace with appropriate redirect
# def discount_success(request):
#     return render(request, 'seller/discount_success.html')



def apply_discount(request):
    if request.method == 'POST':
        discount_type = request.POST.get('discount_type')
        
        try:
            # Convert discount_value to Decimal
            discount_value = Decimal(request.POST.get('discount_value'))
        except (ValueError, TypeError):
            messages.error(request, 'Invalid discount value entered.')
            return redirect('seller_dashboard')

        product_ids = request.POST.getlist('products')

        for product_id in product_ids:
            try:
                product = Product.objects.get(id=product_id)
                original_price = product.original_price
                
                # Set discount type and value
                product.discount_type = discount_type
                product.discount_value = discount_value
                
                # Recalculate the discounted price based on the type of discount
                if discount_type == 'percentage':
                    # Ensure both operands are Decimals
                    product.price = original_price * (1 - discount_value / Decimal(100))
                elif discount_type == 'fixed':
                    product.price = original_price - discount_value
                product.save()
                
            except Product.DoesNotExist:
                messages.error(request, f'Product with ID {product_id} not found.')

        messages.success(request, 'Discount applied successfully to selected products.')
        return redirect('seller_dashboard')

    # If GET request, redirect back to dashboard or show the form again
    return render(request, 'seller_dashboard.html')
