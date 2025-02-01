from django.contrib import admin
from .models import Order,Address,OrderItems,ProductReview


# Register your models here.
admin.site.register(Order)
admin.site.register(Address)
admin.site.register(OrderItems)
admin.site.register(ProductReview)