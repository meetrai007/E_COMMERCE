from django.contrib import admin
from .models import Category, Brand, Tag, Product

# Register Category, Brand, Tag, and Product models
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Tag)
admin.site.register(Product)
