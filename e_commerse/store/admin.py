from django.contrib import admin
from .models import Product, ProductImage, Category

# Register Category model
admin.site.register(Category)

# Inline for ProductImage
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Allow for one extra empty row to add an image in the admin panel

# ProductAdmin class to handle inline images
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ['name', 'category', 'price', 'quantity']
    search_fields = ['name', 'category__name']

# Register Product model with ProductAdmin
admin.site.register(Product, ProductAdmin)

# Register ProductImage model
admin.site.register(ProductImage)
