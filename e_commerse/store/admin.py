from django.contrib import admin
from .models import Category,Product

# Register your models here.
admin.site.register(Category)
class Productadmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
admin.site.register(Product,Productadmin)