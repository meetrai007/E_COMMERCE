from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from seller.models import Seller
from store.models import Product, Category,ProductImage
from django.contrib.auth.models import User
from orders.models import Order
from django.contrib.auth import authenticate, login
from django.core.cache import cache
from base.models import Userprofile

@login_required(login_url="/seller/login/")
def seller_dashboard(request):
    sellername = request.user.username
    seller_id = request.user.seller_id

    # Fetch products and orders
    products = Product.objects.filter(seller=seller_id)
    orders = Order.objects.filter(product__seller=seller_id)
    categories = Category.objects.all()  # Get all categories for dropdown

    # Handle Add Product logic
    if request.method == "POST":
        name = request.POST["name"]
        category_id = request.POST["category"]
        price = request.POST["price"]
        quantity = request.POST["quantity"]
        description = request.POST["description"]
        photos = request.FILES.getlist("photos")  # Get multiple files uploaded

        category = Category.objects.get(id=category_id)
        
        # Create the product
        product = Product.objects.create(
            name=name,
            category=category,
            price=price,
            quantity=quantity,
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

    if request.method == "POST":
        # Get form data
        name = request.POST.get("name")
        category_id = request.POST.get("category")
        price = request.POST.get("price")
        quantity = request.POST.get("quantity")
        description = request.POST.get("description")
        new_photos = request.FILES.getlist("photos")  # Get multiple new images uploaded

        # Validate the form fields
        if not name or not price or not description:
            error_message = "Please fill in all required fields."
            return render(
                request,
                "seller/edit_product.html",
                {
                    "product": product,
                    "categories": categories,
                    "error_message": error_message,
                },
            )

        # Get the selected category
        category = get_object_or_404(Category, id=category_id)

        # Update product details
        product.name = name
        product.category = category
        product.price = price
        product.quantity = quantity
        product.description = description

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
        },
    )