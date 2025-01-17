from django.urls import path
from .views import  seller_dashboard
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('seller-dashboard/', seller_dashboard, name='seller_dashboard'),
    # URL for seller registration
    path('register/', views.seller_register, name='seller_register'),

    # URL for seller login
    path('login/', views.seller_login, name='seller_login'),

    # URL for seller logout
    path('logout/', views.seller_logout, name='seller_logout'),

    path('products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:product_id>/', views.remove_product, name='remove_product'),

    path('remove-product-image/<int:image_id>/', views.remove_product_image, name='remove_product_image'),

    path('apply_discount/', views.apply_discount, name='apply_discount'),
]

